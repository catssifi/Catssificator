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

#from lib.utils import get_base
from datetime import datetime, timedelta
import threading
from lib.config import Config
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import debug, columnize_in_sql_way, build_ordered_by_sql_clause,build_where_sql_clause

import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

class DB_Constants(object):
	tbl_Query_Map = 'Query_Map'
	tbl_Query_Map_col_id = 'rowid'
	tbl_Query_Map_col_query = 'query'
	tbl_Query_Map_col_from_who = 'from_who'
	tbl_Query_Map_col_create_date = 'create_date'
	tbl_Query_Map_col_categories = 'categories'
	tbl_Category = 'Category'
	tbl_Category_col_category_num = 'category_num'
	tbl_Category_col_category = 'category'
	tbl_Submission_Count = 'Submission_Count'
	tbl_Submission_Count_col_day_n = 'day_n'
	tbl_Submission_Count_col_count = 'count'
	
	INCEPTION_DATE = datetime(2015,01,05)

def calculate_day_n_list (date_started_back_to, back_days):
	s = date_started_back_to - timedelta(days=back_days-1)
	ss = s - DB_Constants.INCEPTION_DATE
	start_day_n = ss.days+1
	day_n_list = list()
	for i in xrange(0, back_days):
		day_n_list.append(start_day_n + i)
	return day_n_list

@Singleton
class SQLDatabase(Loggable):
	
	_db_location = None
	_db = None
	_lock = threading.RLock()
	_lock_submission_count = threading.RLock()
	
	def __init__(self):
		if not self._db_location:
			if not hasattr(SQLDatabase, '_db_location') or not SQLDatabase._db_location:
				self._db_location = Config.Instance().get_yaml_data(['db', 'location'], 'database.db')
			else:
				self._db_location = SQLDatabase._db_location	#This is for testing purpose
		self._db = create_engine('sqlite:///%s'%(self._db_location))
		self._db.echo = False  # Try changing this to True and see what happens
		self.info('Initializing SQLiteDatabase object at path: %s' % (self._db_location))
		self.init_sqlite()
		
	def insert_into_query_map(self, query, from_who, categories_str=''):
		sql = '''INSERT INTO %s (query, from_who, create_date, categories) VALUES("%s", "%s", datetime('NOW'), "%s")
				'''         %(DB_Constants.tbl_Query_Map, query, from_who, categories_str)
		self.execute(sql)
		
	def insert_into_category(self, category_num, category):
		sql = ''' INSERT INTO %s (%s, %s) VALUES (%s, "%s")
				''' %(DB_Constants.tbl_Category, DB_Constants.tbl_Category_col_category_num, DB_Constants.tbl_Category_col_category,
					category_num, category)
		self.execute(sql)

	#returns 0 if not found
	# else, returns an non-negative integer indicating the total submissions on day_N	
	def get_submission_count(self, day_n):
		results = self.select_submission_count(day_n)
		if results:
			return results[0][0]
		else:
			return 0

	def get_aggregate_submission_count(self, date_started_back_to=datetime.now(), back_days=1):
		day_n_list = calculate_day_n_list(date_started_back_to, back_days)
		cols_str = ' SUM (%s)' % DB_Constants.tbl_Submission_Count_col_count
		_where_clause_sql = 'where %s in (%s)' %(DB_Constants.tbl_Submission_Count_col_day_n, 
							reduce(lambda x, y: str(x) + ',' + str(y), day_n_list))
		count = self._select_table(DB_Constants.tbl_Submission_Count, cols_str, where_clause_sql=_where_clause_sql)[0][0]
		if count:
			return count
		else:
			return 0

	def select_submission_count(self, day_n):
		cols=[DB_Constants.tbl_Submission_Count_col_count]
		cols_str=columnize_in_sql_way(cols)
		_where_clause_sql='where %s = %s' %(DB_Constants.tbl_Submission_Count_col_day_n, day_n)
		return self._select_table(DB_Constants.tbl_Submission_Count, cols_str, where_clause_sql=_where_clause_sql)

	def decrement_submission_count(self, on_date=datetime.now()):
		diff_in_days = on_date - DB_Constants.INCEPTION_DATE
		self._update_submission_count_on_day_n(diff_in_days.days+1, increment=False)


	def decrement_submission_count_on_day_n(self, day_n):
		self._update_submission_count_on_day_n(day_n, increment=False)

	def increment_submission_count(self, on_date=datetime.now()):
		diff_in_days = on_date - DB_Constants.INCEPTION_DATE
		self._update_submission_count_on_day_n(diff_in_days.days+1, increment=True)

	def increment_submission_count_on_day_n(self, day_n):
		self._update_submission_count_on_day_n(day_n, increment=True)

	def _update_submission_count_on_day_n(self, day_n, increment=True):
		with self._lock_submission_count:
			result_count = self.select_submission_count(day_n)
			count = 1
			sql=None
			if result_count:
				count=result_count[0][0]+ (1 if increment else -1)
				if count>=0:
					sql=''' UPDATE %s SET %s=%s WHERE %s=%s
					''' %(DB_Constants.tbl_Submission_Count, DB_Constants.tbl_Submission_Count_col_count, count,
						DB_Constants.tbl_Submission_Count_col_day_n, day_n)
			else:
				sql = ''' INSERT INTO %s (%s, %s) VALUES (%s, %s)
						''' %(DB_Constants.tbl_Submission_Count, DB_Constants.tbl_Submission_Count_col_day_n
							, DB_Constants.tbl_Submission_Count_col_count, day_n, count)
			if sql:
				self.execute(sql)

	def get_connection(self):
		return sqlite3.connect(self._db_location)

	def count_query_map(self):
		return self._count_table(DB_Constants.tbl_Query_Map)
	
	def _count_table(self, table_name):
		sql = 'select count(1) from %s' % (table_name)
		results = self.execute(sql, return_results=True)
		return results[0][0]

	def select_category(self, category_num=None, category=None):
		cols_str=columnize_in_sql_way([DB_Constants.tbl_Category_col_category_num, DB_Constants.tbl_Category_col_category])
		_where_clause_sql=''
		if category_num or category:
			_where_clause_sql = 'where 1>0'
			if category_num:
				_where_clause_sql += ' and %s = %s' % (DB_Constants.tbl_Category_col_category_num, category_num)
			if category:
				_where_clause_sql += ' and %s = "%s"' % (DB_Constants.tbl_Category_col_category, category)
		return self._select_table(DB_Constants.tbl_Category, cols_str, id=None, where_clause_sql=_where_clause_sql)
		
	def select_query_map(self, where_filter_dict=None, cols=None, id=None, limit=10, offset=0, ordered_column_index=0, ordered_direction=''):
		cols_str=columnize_in_sql_way(cols)
		ordered_column=cols[ordered_column_index]
		where_clause_sql=build_where_sql_clause(where_filter_dict)
		return self._select_table(DB_Constants.tbl_Query_Map, cols_str, DB_Constants.tbl_Query_Map_col_id, id, limit, offset, ordered_column, ordered_direction, where_clause_sql=where_clause_sql)

	def _select_table(self, table_name, cols_str, id_col_name='id', id=None, limit=10, offset=0, ordered_column='', ordered_direction='', where_clause_sql=''):
		ordered_by_sql_clause=build_ordered_by_sql_clause(ordered_column, ordered_direction)
		if id:
			if where_clause_sql:
				where_clause_sql += ' and %s=%s'%(id_col_name, id)
			else:
				where_clause_sql = ' where %s=%s'%(id_col_name, id)
		sql = '''select %s        from %s %s %s LIMIT %s OFFSET %s 
		''' %(  cols_str, table_name, where_clause_sql, ordered_by_sql_clause,  limit,    offset)
		#debug() 
		results = self.execute(sql, return_results=True)
		return results

	def del_query_map_by_id(self, ids):
		ids_str=columnize_in_sql_way(ids)
		sql = ''' DELETE FROM %s WHERE %s in (%s)
		'''                   %(DB_Constants.tbl_Query_Map, DB_Constants.tbl_Query_Map_col_id, ids_str)
		results = self.execute(sql)

	#This method is very danergous! call with caution
	def drop_all_tables(self):
		with self._lock:
			sql = "drop table if exists %s ;"%(DB_Constants.tbl_Query_Map)
			self.execute(sql)
			sql = "drop table if exists %s ;"%(DB_Constants.tbl_Category)
			self.execute(sql)
			sql = "drop table if exists %s ;"%(DB_Constants.tbl_Submission_Count)
			self.execute(sql)

	def init_sqlite(self):
		with self._lock:
			sql = '''
			          CREATE TABLE if not exists %s
			          ( %s INTEGER PRIMARY KEY ASC, %s TEXT NOT NULL, %s VARCHAR(80), %s DATETIME, %s VARCHAR(40)) 
			     ''' % (DB_Constants.tbl_Query_Map, DB_Constants.tbl_Query_Map_col_id, DB_Constants.tbl_Query_Map_col_query, DB_Constants.tbl_Query_Map_col_from_who, DB_Constants.tbl_Query_Map_col_create_date, DB_Constants.tbl_Query_Map_col_categories)
			self.execute(sql)
			
			sql = '''
						CREATE TABLE if not exists %s
			          (%s SMALLINT NOT NULL, %s VARCHAR(80) NOT NULL)
					''' % (DB_Constants.tbl_Category, DB_Constants.tbl_Category_col_category_num, DB_Constants.tbl_Category_col_category)
			self.execute(sql)
			
			sql = '''
						CREATE TABLE if not exists %s
			          (%s SMALLINT NOT NULL, %s INTEGER NOT NULL)
					''' % (DB_Constants.tbl_Submission_Count, DB_Constants.tbl_Submission_Count_col_day_n, DB_Constants.tbl_Submission_Count_col_count)
			self.execute(sql)
		
	def execute(self, sql_statement, return_results=False):
		results=None
		conn = self.get_connection()
		c = conn.cursor()
		c.execute(sql_statement)
		if return_results:
			results=c.fetchall()
		conn.commit()
		conn.close()
		return results