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

from datetime import datetime
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))
from backend.database import SQLDatabase, DB_Constants
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
		result = self._sqldb.select_query_map(cols=[DB_Constants.tbl_Query_Map_col_id, DB_Constants.tbl_Query_Map_col_query, DB_Constants.tbl_Query_Map_col_categories])
		#debug()
		self.assertEqual(result[3][1], query)
		
		#Now test the offset and limit
		result = self._sqldb.select_query_map(cols=[DB_Constants.tbl_Query_Map_col_id, DB_Constants.tbl_Query_Map_col_query], limit=1, offset=3)
		self.assertEqual(result[0][1], query)
		
		id=result[0][0]
		#debug()
		self._sqldb.del_query_map_by_id([1, id])
		result = self._sqldb.select_query_map(cols=[DB_Constants.tbl_Query_Map_col_id])
		self.assertEqual(len(result), 2)	#removed two, should have only 2 records
		
		count = self._sqldb.count_query_map()
		self.assertEqual(count, 2)
	
	def test_submission_counts(self):
		day_N=10
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 0)
		
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 3)
		
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 1)
		
		self._sqldb.increment_submission_count_on_day_n(day_N)
		#debug()
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 0)
		
		#debug()
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 4)
		
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.increment_submission_count_on_day_n(day_N)
		self.assertEqual(count, 4)
		
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		self._sqldb.decrement_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 0)
		
		self._sqldb.increment_submission_count_on_day_n(day_N)
		count = self._sqldb.get_submission_count(day_N)
		self.assertEqual(count, 1)
		
	def test_aggregate_submission_counts(self):
		day_1 = 1	#it means on the INCEPTION_DAY
		day_2 = 2	#it means on the INCEPTION_DAY + 1
		day_3 = 3	#it means on the INCEPTION_DAY + 2
		
		self._sqldb.increment_submission_count_on_day_n(day_3)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.increment_submission_count_on_day_n(day_2)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.increment_submission_count_on_day_n(day_2)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		self._sqldb.decrement_submission_count_on_day_n(day_1) # this is minus
		self._sqldb.increment_submission_count_on_day_n(day_2)
		self._sqldb.increment_submission_count_on_day_n(day_1)
		
		count = self._sqldb.get_submission_count(day_1)
		self.assertEqual(count, 6)
		count = self._sqldb.get_submission_count(day_2)
		self.assertEqual(count, 3)
		count = self._sqldb.get_submission_count(day_3)
		self.assertEqual(count, 1)
		
		#Now do the fun parts: calculate the aggregate submission counts
		DB_Constants.INCEPTION_DATE = datetime(2010,01,01)
		_date_started_back_to = datetime(2010, 01, 03)
		_back_days=3
		agg_count = self._sqldb.get_aggregate_submission_count(date_started_back_to=_date_started_back_to, back_days=_back_days)
		self.assertEqual(agg_count, 10)
		
	def test_aggregate_submission_counts_on_today(self):
		DB_Constants.INCEPTION_DATE = datetime(2011,01,01)
		fake_today = datetime(2011,01, 05)
		self._sqldb.increment_submission_count(fake_today)
		self._sqldb.increment_submission_count(fake_today)
		self._sqldb.decrement_submission_count(fake_today)
		self._sqldb.increment_submission_count(fake_today)
		self._sqldb.increment_submission_count(fake_today)
		
		count = self._sqldb.get_submission_count(5)
		self.assertEqual(count, 3)
		
		