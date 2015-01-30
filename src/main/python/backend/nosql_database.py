#!/usr/bin/python
# Copyright (c) 2015 Ken Wu
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

from lib.config import Config
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import debug,clear_dir
from CodernityDB.database_thread_safe import ThreadSafeDatabase
from CodernityDB.hash_index import HashIndex
from CodernityDB.database import RecordNotFound

class NOSQL_DB_Constants(object):

	tbl_WORD = 'Word_Tag'
	tbl_WORD_Noun_Noun_Similarity = 'Noun_Noun_Similarity'
	
	tbl_Processed_File = 'Processed_File'
	
	tbl_New_Vocab = 'New_Vocab'

#This is an abstract Database class 
class NoSQLDatabase(Loggable):
	_db_location = None
	_db = None

class WordTagIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(WordTagIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        if data['t'] == 'Word_Tag':
            wt = data['word_tag']
            # if not isinstance(login, basestring):
            #     login = str(login)
            return md5(wt).digest(), {'word_tag': data['word_tag'], 'word_tag_map': data['word_tag_map']}

    def make_key(self, key):
        return md5(key).digest()

class NounNounSimilarityIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(NounNounSimilarityIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        if data['t'] == 'Noun_Noun_Similarity':
            wx = data['noun_x']
            return md5(wx).digest(), {'noun_x': data['noun_x'], 'noun_ys': data['noun_ys']}

    def make_key(self, key):
        return md5(key).digest()

class ProcessedFileIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(ProcessedFileIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        if data['t'] == 'Processed_File':
            m = data['md5']
            return md5(m).digest(), {'md5': data['md5'], 'file_path': data['file_path'], 'processed_date': data['processed_date']}

    def make_key(self, key):
        return md5(key).digest()


class NewVocabIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '16s'
        super(NewVocabIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        if data['t'] == 'New_Vocab':
            wt = data['new_vocab']
            # if not isinstance(login, basestring):
            #     login = str(login)
            return md5(wt).digest(), {'new_vocab': data['new_vocab']}

    def make_key(self, key):
        return md5(key).digest()

@Singleton
class AI_NoSqlDatabase(NoSQLDatabase):

	def __init__(self):
		if not self._db_location:
			if not hasattr(AI_NoSqlDatabase, '_db_location') or not AI_NoSqlDatabase._db_location:
				self._db_location = Config.Instance().get_yaml_data(['db-ai', 'location'], 'database-ai.db')
			else:
				self._db_location = AI_NoSqlDatabase._db_location	#This is for testing purpose
		self.init_database()
		
	def close_db(self):
		self._db.close()
	
	def earse_db(self):
		self.close_db()
		clear_dir(self._db_location)
	
	def init_database(self):
		self.info('Initializing AI_NoSqlDatabase object at path: %s for AI part' % (self._db_location))
		self._db = ThreadSafeDatabase(self._db_location)
		db = self._db
		
		if db.exists():
			self.info('DB exists..')
			db.open()
			db.reindex()
		else:
			self.info('DB NOT exists..now creating.')
			db.create()
			db.add_index(WordTagIndex(db.path, NOSQL_DB_Constants.tbl_WORD))
			db.add_index(NounNounSimilarityIndex(db.path, NOSQL_DB_Constants.tbl_WORD_Noun_Noun_Similarity))
			db.add_index(ProcessedFileIndex(db.path, NOSQL_DB_Constants.tbl_Processed_File))
			db.add_index(NewVocabIndex(db.path, NOSQL_DB_Constants.tbl_New_Vocab))
			
			
	def add_to_noun_noun_map(self, doc):
		doc['t'] = NOSQL_DB_Constants.tbl_WORD_Noun_Noun_Similarity
		return self._db.insert(doc)
	
	def add_to_word_tag_map(self, doc):
		doc['t'] = NOSQL_DB_Constants.tbl_WORD
		return self._db.insert(doc)
	
	def add_to_processed_path(self, doc):
		doc['t'] = NOSQL_DB_Constants.tbl_Processed_File
		return self._db.insert(doc)
	
	def add_to_new_vocab(self, doc):
		doc['t'] = NOSQL_DB_Constants.tbl_New_Vocab
		return self._db.insert(doc)
	
	def get_from_noun_noun(self, noun_x):
		return self._get(NOSQL_DB_Constants.tbl_WORD_Noun_Noun_Similarity, noun_x, with_doc=True)
		
	def get_from_word_tag(self, word_tag):
		return self._get(NOSQL_DB_Constants.tbl_WORD, word_tag, with_doc=True)
		
	def get_from_processed_file(self, md5):
		return self._get(NOSQL_DB_Constants.tbl_Processed_File, md5, with_doc=True)
	
	def get_from_new_vocab(self, w):
		return self._get(NOSQL_DB_Constants.tbl_New_Vocab, w, with_doc=True)
	
		
	def _get(self, index_name, key, with_doc):
		try: 
			return self._db.get(index_name, key, with_doc=with_doc)
		except RecordNotFound as e:
			return None
	
	def update(self, doc):
		self._db.update(doc)
	