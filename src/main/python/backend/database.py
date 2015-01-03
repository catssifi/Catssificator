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
tbl_Query_Map = 'Query_Map'
tbl_Category = "Category"

@Singleton
class SQLDatabase(Loggable):

	global tbl_Query_Map
	global tbl_Category
	
	
	_db_location = None
	_db = None
	_lock = threading.RLock()
	
	def __init__(self):
		if not self._db_location:
			if not SQLDatabase._db_location:
				self._db_location = Config.Instance().get_yaml_data(['db', 'location'], 'database.db')
			else:
				self._db_location = SQLDatabase._db_location	#This is for testing purpose
		self._db = create_engine('sqlite:///%s'%(self._db_location))
		self._db.echo = False  # Try changing this to True and see what happens
		self.info('Initializing SQLiteDatabase object at path: %s' % (self._db_location))
		self.init_sqlite()
		
	def insert_into_query_map(self, query, from_who, categories=''):
		sql = '''INSERT INTO %s (query, from_who, create_date, categories) VALUES("%s", "%s", datetime('NOW'), "%s")
				'''         %(tbl_Query_Map, query, from_who, categories)
		self.execute(sql)
		pass

	def get_connection(self):
		return sqlite3.connect(self._db_location)

	def select_query_map(self, cols=None, id=None, limit=10, offset=0):
		cols_str=columnize_in_sql_way(cols)
		return self._select_table(tbl_Query_Map, cols_str, id, limit, offset)

	def _select_table(self, table_name, cols_str, id=None, limit=10, offset=0):
		sql = '''select %s        from %s LIMIT %s OFFSET %s 
				''' %(  cols_str, table_name,   limit,    offset) 
		results = self.execute(sql, return_results=True)
		return results

	def del_query_map_by_id(self, ids):
		ids_str=columnize_in_sql_way(ids)
		sql = ''' DELETE FROM %s WHERE id in (%s)
		'''                   %(tbl_Query_Map, ids_str)
		results = self.execute(sql)

	#This method is very danergous! call with caution
	def drop_all_tables(self):
		with self._lock:
			sql = "drop table if exists %s ;"%(tbl_Query_Map)
			self.execute(sql)
			sql = "drop table if exists %s ;"%(tbl_Category)
			self.execute(sql)

	def init_sqlite(self):
		with self._lock:
			sql = '''
			          CREATE TABLE if not exists %s
			          (id INTEGER PRIMARY KEY ASC, query TEXT NOT NULL, from_who VARCHAR(80), create_date DATETIME, categories VARCHAR(40)) 
			          ''' % (tbl_Query_Map)
			self.execute(sql)
			
			sql = '''
						CREATE TABLE if not exists %s
			          (category_num SMALLINT NOT NULL, category VARCHAR(80) NOT NULL)
					''' % (tbl_Category)
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