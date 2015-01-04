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
from backend.database import SQLDatabase
from lib.utils import *
import unittest

class SQLDatabaseTest(unittest.TestCase):

	#_test_path=join(abspath(dirname('__file__')), '../../../data/test/')
	_sqldb = None

	def setUp(self):
		self._sqldb=SQLDatabase.Instance()
		self._sqldb.drop_all_tables()	#drop all tables to have a fresh start
		self._sqldb.init_sqlite()		#recreate it back

	def test_put_and_delete(self):
		self._sqldb.insert_into_query_map('This iphone is quite expensive', '127.0.0.1')
		self._sqldb.insert_into_query_map('This andriod is absolutely expensive', '127.0.0.1')
		self._sqldb.insert_into_query_map('Do not abuse dogs!', '127.0.0.1')
		query='Cats are human\'s friends & soulmates'
		self._sqldb.insert_into_query_map(query, '127.0.0.1')    	
		result = self._sqldb.select_query_map(cols=['query'])
		self.assertEqual(result[3][0], query)
		
		#Now test the offset and limit
		result = self._sqldb.select_query_map(cols=['id', 'query'], limit=1, offset=3)
		self.assertEqual(result[0][1], query)
		
		id=result[0][0]
		#debug()
		self._sqldb.del_query_map_by_id([1, id])
		result = self._sqldb.select_query_map(cols=['id'])
		self.assertEqual(len(result), 2)	#removed two, should have only 2 records
		
		count = self._sqldb.count_query_map()
		self.assertEqual(count, 2)
		
		