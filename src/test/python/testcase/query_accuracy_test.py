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
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))
from backend.file_datastore import *
from backend.datastore import *
from lib.utils import *
from query_processor import QueryProcessor 
from backend.category import Category, replace_category_num_with_name
from backend.database import SQLDatabase,DB_Constants
from web.constants import JSON_API_Constants
import unittest

tech_category='Technology'
mobile_devices_category='Mobile_Devices'
hardware_category='Hardware'

class QueryAccuracyTest(unittest.TestCase):
    
    _test_path=join(abspath(dirname('__file__')), '../../../data/test/')
    _test_file='test-backend'
    _qp = None
    _fds = None
    _category = None
    
    def setUp(self):
        clear_dir(self._test_path)
        self._fds=FileDataStore(self._test_path+self._test_file)
        self._category=Category.Instance()
        self._category.set_path(join(abspath(dirname('__file__')), '../../../config/test/')+'test-category.txt')
        self._qp = QueryProcessor(self._fds)
        SQLDatabase.Instance().drop_all_tables()    #drop all tables to have a fresh start
        SQLDatabase.Instance().init_sqlite()        #recreate it back
        
    def test_query_strengths(self):
        query='IPHONE'
        self.assertEqual(self._qp.inquire(query)['result'], 'no')   #made sure it starts from empty first
        self._qp.submit(query, mobile_devices_category)
        self.assertEqual(self._qp.inquire(query)[JSON_API_Constants.category], mobile_devices_category)   #made sure it now has a assigned category
        
        query='Today my iphone is broken, i am taking it to for repair in a local brooklyn shop'
        self.assertEqual(self._qp.inquire(query)[JSON_API_Constants.category], mobile_devices_category)   #made sure this query now has a assigned category: mobile devices
        self._qp.submit(query, hardware_category)       #Now submit this query to the hardware_category
        
        query='my dad\'s iphone is broken as well...searching for a cheap repair shop'
        self._qp.submit(query, hardware_category)       #Now submit this query to the hardware_category
        
        
        query='IPHONE'
        results = self._qp.inquire(query)
        self.assertEqual(results[JSON_API_Constants.category], mobile_devices_category)   #It should belong to the mobile_devices category since the previous two queries are nosier than the first one
        
        
    def tearDown(self):
        self._category.set_path(join(abspath(dirname('__file__')), '../../../config/test/')+'test-category-production.txt')