# Copyright 2019 TWO SIGMA OPEN SOURCE, LLC
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


import unittest

import pandas as pd

from ..chart import TimePlot, Line
from ..plotitem import ConstantLine


class TestTimePlot(unittest.TestCase):

    def test_plot(self):
        # given
        # when
        plot = TimePlot(timeZone="America/New_York")

        # then
        model = plot.model
        self.assertEqual(model['timezone'], "America/New_York")

        self.assertEqual(len(model['rangeAxes']), 1)
        self.assertEqual(len(model['texts']), 0)
        self.assertEqual(len(model['constant_lines']), 0)
        self.assertEqual(len(model['constant_bands']), 0)
        self.assertEqual(len(model['graphics_list']), 0)

    def test_add_Line_to_plot(self):
        # given
        plot = TimePlot()
        # when
        plot.add(Line())
        # then
        model = plot.model
        self.assertEqual(len(model['graphics_list']), 1)

    def test_add_ConstantLine_to_plot_with_pandas_date_time(self):
        # given
        plot = TimePlot()
        # when
        plot.add(ConstantLine(x=pd.to_datetime('2015-02-04 15:00:00')))
        # then
        self.assertEqual(plot.model['constant_lines'][0]['x'], 1423062000000)
