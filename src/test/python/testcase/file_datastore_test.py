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
import unittest

class FileDataStoreTest(unittest.TestCase):

    _test_path=join(abspath(dirname('__file__')), '../../../data/test/')
    _test_file='test-backend'
    _fds = None

    def setUp(self):
        clear_dir(self._test_path)
        self._fds=FileDataStore(self._test_path+self._test_file)

    def test_get_from_empty(self):
        self.assertEqual(self._fds.get("Iphone"), None)
        self.assertEqual(self._fds.get("Android"), None)
    
    def test_store_and_retrieve_lv1(self):
        self._fds.set_retrieve_categories_level(1)
        #debug()
        self._fds.store('IPad', 1.0, [1,5,7])    #Storing the word 'IPad' to category num 1 and 5 and 7
        self._fds.store('IPad', 1.0, [2,7])    #Storing the word 'IPad' to category num 2 and 7
        self._fds.store('IPad', 1.0, [2,7,10])    #Storing the word 'IPad' to category num 2 and 7 and 10
        self._fds.store('IPad', 1.0, [8,10])    #Storing the word 'IPad' to category num 8 and 10
        
        self.assertEqual(self._fds.get("IPad",7), 3.0)    
        self.assertEqual(self._fds.get("IPad",10), 2.0)     
        self.assertEqual(self._fds.get("IPad",1), 1.0)
        
        self.assertEqual(self._fds.get("IPad",highest_score_only=True), [7])
    
        self._fds.store('Surface', 1.0, [9,6])
        self._fds.store('IPad', 1.0, [2,8])
        self._fds.store('Surface', 1.0, [9])
        self._fds.store('Surface', 1.0, [9])
        self._fds.store('Surface', 1.0, [9,6])
        self._fds.store('IPad', 1.0, [2,11])
        self._fds.store('IPad', 1.0, [11])
        
        self.assertEqual(self._fds.get("IPad",highest_score_only=True), [2.0])
        self.assertEqual(self._fds.get("Surface",highest_score_only=True), [9.0])

        #now change the level to 3
        self._fds.set_retrieve_categories_level(3)
        self.assertEqual(self._fds.get("IPad", highest_score_only=True), [2,7,8])
        self.assertEqual(self._fds.get("Surface", highest_score_only=True), [9,6]) 