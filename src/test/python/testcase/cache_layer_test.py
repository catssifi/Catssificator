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
from web.cache import Cache
from backend.database import SQLDatabase
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))
import unittest

class CacheLayerTest(unittest.TestCase):
    
    def setUp(self):
        self.reinit_the_database()
    
    def reinit_the_database(self):
        SQLDatabase.Instance().drop_all_tables()
        SQLDatabase.Instance().init_sqlite()
        
    
    def test_get_submissions_today(self):
        SQLDatabase.Instance().increment_submission_count()
        SQLDatabase.Instance().increment_submission_count()
        SQLDatabase.Instance().increment_submission_count()
        count = Cache.Instance().get_submissions_today()
        self.assertEqual(count, 3)  #make sure it has count 3 to start with
        self.reinit_the_database()  #earse everything from the database
        count = Cache.Instance().get_submissions_today()
        self.assertEqual(count, 3)  #It should still read 3 since it is still in the cache
        
        count = Cache.Instance().get_submissions_today(refresh=True)
        self.assertEqual(count, 0)  #should be empty after refreshing from database
    
    def test_get_submissions_in_the_past_n_days(self):
        SQLDatabase.Instance().increment_submission_count()
        count = Cache.Instance().get_submissions_in_the_past_n_days(3)
        self.assertEqual(count, 1)  #should be empty after refreshing from database
    
        