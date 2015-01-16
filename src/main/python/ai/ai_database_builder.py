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
import collections
import threading
from lib.utils import debug, real_lines,get_file_name_from_path,get_line_and_md5_from_file, words
from lib.singleton import Singleton
from lib.loggable import Loggable
from backend.database import SQLDatabase_AI 

@Singleton
class AIDatabaseBuilder(Loggable):
    
    _db = None
    #_words_counts_model = None
    #_lock_words_counts_model = threading.RLock()
    
    def __init__(self):
        self._db = SQLDatabase_AI.Instance()
    
    #This is danergous! it should be called with very caution
    def reset_whole_database(self):
        self._db.drop_all_tables()
        self._db.init_sqlite()
    
    
    def _build_words_count(self, line):
        model = collections.defaultdict(lambda: 1)
        for f in line:
            model[f] += 1
        return model
    
    #This method is to add all the word counts to the internal database
    #It returns the number of the words inserted into the database
    def add_build_from_file(self, file_path):
        file_name=get_file_name_from_path(file_path)
        (all_contents_in_one_line,md5_str) = get_line_and_md5_from_file(file_path)
        if not self._db.exists_in_processed_path(file_name, md5_str):
            model = self._build_words_count(words(all_contents_in_one_line))
            inserted = self._db.insert_or_replace_words_count(model)
            self._db.insert_processed_path(file_name, md5_str)
            return inserted
        else:
            self.warn('file: %s has been processed...' %(file_path))
            return None
    
    def load_words_counts_model(self):
        d={}
        results = self._db.select_words_counts()
        if results:
            for item in results: 
                d[item[0]]=item[1]
        self._words_counts_model = d
        return d