#!/usr/bin/python
# Copyright (c) 2014 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu
# Date: 2014 Dec - 2015

import sys
from lib.utils import debug
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))
from request_ticket_system import RequestTicketSystem
import unittest

class RequestTicketSystemTest(unittest.TestCase):
    
    _rts = RequestTicketSystem.Instance()
    
    def setUp(self):
        pass
    
    def test_1(self):
        self._rts.clean_up()
        ticket_1=self._rts.generate_category_ticket('iphone', ['iphone'])
        ticket_2=self._rts.generate_category_ticket('android', ['android'])
        ticket_2=self._rts.generate_category_ticket('ipad', ['ipad'])
        size = self._rts.size()
        self.assertEqual(size, 3)
        self._rts.clean_up()
        size = self._rts.size()
        self.assertEqual(size, 0)
        