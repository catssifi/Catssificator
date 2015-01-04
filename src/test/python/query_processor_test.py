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
from backend.category import Category
from backend.database import SQLDatabase
import unittest

class QueryProcessorTest(unittest.TestCase):
    
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
        
    def test_query_processing(self):
        query='look for a IPHONE'
        words = self._qp.process_query(query)
        self.assertEqual(words, ['look', 'iphon'])   #should find nothing first
        
    def test_query_answer_1(self):
        query='Iphone good one'
        ans = self._qp.inquire(query)
        self.assertEqual(get_json_value(ans, 'result'), 'no')   #should find nothing first
        
        cn_md = self._category.get_num('Mobile_Devices')
        self._fds.store('iphone', cn_md)
        self._fds.store('sucks', cn_md)
        
        ans = self._qp.inquire(query)       #ask again, it should return Mobile_Devices
        self.assertEqual(get_json_value(ans, 'category'), 'Mobile_Devices')   #should find it as Mobile_Devices
        
        cn_t =  self._category.get_num('Technology')
        self._fds.store('java', cn_t)
        self._fds.store('sucks', cn_t)
        
        query2='java is hard?'
        ans = self._qp.inquire(query2)       #ask again, it should return Mobile_Devices
        self.assertEqual(get_json_value(ans, 'category'), 'Technology')   #should find it as Technology
        
    
    def test_submit(self):
        query_submit='Amazon kindle good sales'
        category='Technology'
        self._qp.submit(query_submit, category, from_who='localhost')
        result = SQLDatabase.Instance().select_query_map(cols=['query'])
        self.assertEqual(len(result), 1)
    
        query_submit='Is Thailand good'
        category='Travel'
        self._qp.submit(query_submit, category, from_who='localhost')
        
        query='is amazon good'
        ans=self._qp.inquire(query)
        self.assertEqual(get_json_value(ans, 'result'), 'yes')   #should find it as Technology
        self.assertEqual(get_json_value(ans, 'category'), 'Technology')   #should find it as Technology
        
        category_invalid='Porn'                                 #Try to submit to some invalid nonexist category
        sub_ans=self._qp.submit(query_submit, category_invalid, from_who='localhost2')
        self.assertEqual(get_json_value(sub_ans, 'result'), 'no')   #should not find it
        
        result = SQLDatabase.Instance().select_query_map(cols=['query'])
        self.assertEqual(len(result), 2)    #should have 2 records in total from this method
    
        
    def test_stemming_word_query_answer(self):
        query_submit='I repaired an macbook pro'
        category='Hardware'
        self._qp.submit(query_submit, category, from_who='localhost2')    
        
        query='monitor repairment'
        ans=self._qp.inquire(query)
        self.assertEqual(get_json_value(ans, 'category'), 'Hardware')   #should find it as Hardware since repairment is same as repair after being stemmed
            
        