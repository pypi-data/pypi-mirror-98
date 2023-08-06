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
# See the License for the specific language governing permissions and
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import os
import sys

from beakerx.spark.spark_listener import SparkListener
from beakerx.spark.spark_progress_bar import SparkStateProgressUiManager


class SparkEngine:
    STOP = "stop"
    STOP_FROM_UI = "stop_from_spark_ui_form_button"

    def __init__(self, builder, single_spark_session, spark_session_factory):
        self.spark_session_factory = spark_session_factory
        self.single_spark_session = single_spark_session
        if builder is None:
            raise Exception('value can not be None')
        else:
            self.user_builder = builder
        self.auto_start = False
        self.additional_spark_options = {}
        self.builder = None
        self.uiWebUrlFunc = self._create_ui_web_url()
        self.stop_context = SparkEngine.STOP

    def new_spark_builder(self):
        self.stop_context = SparkEngine.STOP
        self.uiWebUrlFunc = self._create_ui_web_url()
        self.builder = self.spark_session_factory.builder()

    def get_user_spark_config(self):
        return copy.deepcopy(self.user_builder._options)

    def add_additional_spark_options(self, options):
        self.additional_spark_options = options

    def get_additional_spark_options(self):
        return copy.deepcopy(self.additional_spark_options)

    def config(self, name, value):
        self.builder.config(name, value)

    def getOrCreate(self):
        return self.builder.getOrCreate()

    def spark_app_id(self):
        return self.getOrCreate().sparkContext._jsc.sc().applicationId()

    def get_ui_web_url(self):
        return self.uiWebUrlFunc(self.getOrCreate())

    def stop(self):
        self.stop_context = SparkEngine.STOP_FROM_UI
        self.getOrCreate().sparkContext.stop()

    def is_auto_start(self):
        return self.auto_start

    def configure_auto_start(self):
        self.auto_start = True

    def is_active_spark_session(self):
        return self.single_spark_session.active

    def activate_spark_session(self):
        self.single_spark_session.active = True

    def inactivate_spark_session(self):
        self.single_spark_session.active = False

    def configure_listeners(self, sparkui, server):
        spark_session = sparkui.engine.getOrCreate()
        spark_context = spark_session.sparkContext
        spark_context._gateway.start_callback_server()
        spark_context._jsc.sc().addSparkListener(
            SparkListener(sparkui, SparkStateProgressUiManager(sparkui.engine, server)))

    def _create_ui_web_url(self):
        return lambda spark_session: spark_session.sparkContext.uiWebUrl

    def _configure_yarn(self):
        path_to_python = sys.executable
        os.environ["PYSPARK_PYTHON"] = path_to_python
        os.environ["PYSPARK_DRIVER_PYTHON"] = path_to_python
        self.uiWebUrlFunc = lambda spark_session: spark_session.sparkContext._conf._jconf.get(
            "spark.org.apache.hadoop.yarn.server.webproxy.amfilter.AmIpFilter.param.PROXY_URI_BASES")

    def configure_runtime(self):
        if "spark.master" in self.builder._options and "yarn" in self.builder._options["spark.master"]:
            self._configure_yarn()
            return None
