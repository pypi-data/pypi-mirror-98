# Copyright 2019 TWO SIGMA OPEN SOURCE, LLC  #
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

from beakerx_base import BeakerxButton
from traitlets import Unicode


class RESTButton(BeakerxButton):
    _view_name = Unicode('RESTButtonView').tag(sync=True)
    _model_name = Unicode('RESTButtonModel').tag(sync=True)
    _view_module = Unicode('beakerx').tag(sync=True)
    _model_module = Unicode('beakerx').tag(sync=True)
    tooltip = Unicode('tooltip').tag(sync=True)
    url = Unicode('url').tag(sync=True)

    def __init__(self, **kwargs):
        super(RESTButton, self).__init__(**kwargs)
