# Copyright 2020 TWO SIGMA OPEN SOURCE, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

from beakerx.spark.spark_server import BeakerxSparkServer
from beakerx_base import BeakerxBox
from traitlets import Unicode, List, Bool, Dict


class SparkUI(BeakerxBox):
    ONE_SPARK_SESSION_MSG_ERROR = "Cannot have more than one Spark session open in the same notebook."

    _view_name = Unicode('SparkUIView').tag(sync=True)
    _model_name = Unicode('SparkUIModel').tag(sync=True)
    _view_module = Unicode('beakerx').tag(sync=True)
    _model_module = Unicode('beakerx').tag(sync=True)
    profiles = List().tag(sync=True)
    current_profile = Unicode("").tag(sync=True)
    is_auto_start = Bool().tag(sync=True)
    user_spark_conf = Dict().tag(sync=True)

    def __init__(self, engine, ipython_manager, spark_server_factory, profile, comm=None, **kwargs):
        if comm is not None:
            self.comm = comm
        self.engine = self.check_is_None(engine)
        self.ipython_manager = self.check_is_None(ipython_manager)
        self.spark_server_factory = self.check_is_None(spark_server_factory)
        self.profile = self.check_is_None(profile)
        self.on_msg(self.handle_msg)
        self.profiles, self.current_profile = self._get_init_profiles()
        self.user_spark_conf = self.get_user_spark_conf()
        self.is_auto_start = self.engine.is_auto_start()
        super(SparkUI, self).__init__(**kwargs)

    def get_user_spark_conf(self):
        spark_options = self._get_current_profile()
        spark_options.update(self.engine.get_additional_spark_options())
        spark_options.update(self.engine.get_user_spark_config())
        return spark_options

    def handle_msg(self, _, content, buffers=None):
        try:
            if content['event'] == "start":
                self._handle_start(content)
            elif content['event'] == "stop":
                self._handle_stop(content)
            elif content['event'] == "save_profiles":
                self._handle_save_profile(content)
        except Exception as err:
            self.send_error(str(err))

    def _handle_save_profile(self, content):
        payload = content["payload"]
        result, err = self.profile.save(payload)
        if result:
            msg = {
                'method': 'update',
                'event': {
                    "save_profiles": "done"
                }
            }
            self.comm.send(data=msg)

    def _handle_stop(self, content):
        self.engine.stop()

    def end_application(self):
        self.engine.inactivate_spark_session()
        msg = {
            'method': 'update',
            'event': {
                self.engine.stop_context: "done"
            }
        }
        self.comm.send(data=msg)

    def _handle_auto_start(self):
        spark_options = self._get_current_profile()
        spark_options.update(self.engine.get_user_spark_config())
        self.engine.new_spark_builder()
        for key, value in spark_options.items():
            if key == "properties":
                for item in value:
                    self.engine.config(item['name'], item['value'])
            else:
                self.engine.config(key, value)
        err = self._on_start()
        if err is not None:
            self.send_error(err)
            return
        self._send_start_done_event("auto_start")

    def _handle_start(self, content):
        current_profile = content['payload']['current_profile']
        spark_options = content['payload']['spark_options']
        self.engine.new_spark_builder()
        for key, value in spark_options.items():
            if key == "properties":
                for item in value:
                    self.engine.config(item['name'], item['value'])
            else:
                self.engine.config(key, value)
        err = self._on_start()
        if err is not None:
            self.send_error(err)
            return
        self._send_start_done_event("start")
        self.profile.save_current_profile(current_profile)

    def send_error(self, message):
        msg = {
            'method': 'update',
            'error': {
                "message": message
            }
        }
        self.comm.send(data=msg)

    def _on_start(self):
        if self.engine.is_active_spark_session():
            return SparkUI.ONE_SPARK_SESSION_MSG_ERROR
        self.engine.configure_runtime()
        self.ipython_manager.configure(self.engine)
        server = self.spark_server_factory.run_new_instance(self.engine)
        self.engine.configure_listeners(self, server)
        self.engine.activate_spark_session()
        return None

    def _send_start_done_event(self, event_name):
        msg = {
            'method': 'update',
            'event': {
                event_name: "done",
                "sparkAppId": self.engine.spark_app_id(),
                "sparkUiWebUrl": self.engine.get_ui_web_url()
            }
        }
        self.comm.send(data=msg)

    def after_display(self):
        if self.engine.is_auto_start():
            self._handle_auto_start()

    def check_is_None(self, value):
        if value is None:
            raise Exception('value can not be None')
        return value

    def _get_init_profiles(self):
        data, err = self.profile.load_profiles()
        if err is None:
            return data["profiles"], data["current_profile"]
        return [], "", err

    def _get_current_profile(self):
        spark_options = list(filter(lambda x: x['name'] == self.current_profile, self.profiles))
        if len(spark_options) > 0:
            return copy.deepcopy(spark_options.pop(0))
        else:
            return {}


class SparkJobRunner:
    def _task(self, spark_job, ipython, builder, spark_server):
        spark_job(ipython, builder, spark_server)

    def run(self, spark_job, ipython, builder, spark_server):
        self._task(spark_job, ipython, builder, spark_server)


class ServerRunner:

    def _start_server(self, server):
        server.run()

    def run(self, server):
        from threading import Thread
        t = Thread(target=self._start_server, args=(server,))
        t.daemon = True
        t.start()


class BeakerxSparkServerFactory:

    def run_new_instance(self, engine):
        spark_session = engine.getOrCreate()
        spark_context = spark_session.sparkContext
        server = BeakerxSparkServer(spark_context)
        ServerRunner().run(server)
        return server


class IpythonManager:
    def __init__(self, ipython):
        self.ipython = ipython

    def configure(self, engine):
        spark_session = engine.getOrCreate()
        sc = spark_session.sparkContext
        self.ipython.push({"spark": spark_session})
        self.ipython.push({"sc": sc})
        return sc
