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
import threading
from lib.config import Config
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import debug, columnize_in_sql_way

import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

class DB_Constants(object):
	tbl_Query_Map = 'Query_Map'
	tbl_Query_Map_col_id = 'id'
	tbl_Query_Map_col_query = 'query'
	tbl_Query_Map_col_from_who = 'from_who'
	tbl_Query_Map_col_create_date = 'create_date'
	tbl_Query_Map_col_categories = 'categories'
	tbl_Category = 'Category'
	tbl_Category_col_category_num = 'category_num'
	tbl_Category_col_category = 'category'

@Singleton
class SQLDatabase(Loggable):
	
	_db_location = None
	_db = None
	_lock = threading.RLock()
	
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
		pass

	def get_connection(self):
		return sqlite3.connect(self._db_location)

	def count_query_map(self):
		return self._count_table(DB_Constants.tbl_Query_Map)
	
	def _count_table(self, table_name):
		sql = 'select count(1) from %s' % (table_name)
		results = self.execute(sql, return_results=True)
		return results[0][0]


	def select_query_map(self, cols=None, id=None, limit=10, offset=0):
		cols_str=columnize_in_sql_way(cols)
		return self._select_table(DB_Constants.tbl_Query_Map, cols_str, id, limit, offset)

	def _select_table(self, table_name, cols_str, id=None, limit=10, offset=0):
		sql = '''select %s        from %s LIMIT %s OFFSET %s 
				''' %(  cols_str, table_name,   limit,    offset) 
		results = self.execute(sql, return_results=True)
		return results

	def del_query_map_by_id(self, ids):
		ids_str=columnize_in_sql_way(ids)
		sql = ''' DELETE FROM %s WHERE id in (%s)
		'''                   %(DB_Constants.tbl_Query_Map, ids_str)
		results = self.execute(sql)

	#This method is very danergous! call with caution
	def drop_all_tables(self):
		with self._lock:
			sql = "drop table if exists %s ;"%(DB_Constants.tbl_Query_Map)
			self.execute(sql)
			sql = "drop table if exists %s ;"%(DB_Constants.tbl_Category)
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