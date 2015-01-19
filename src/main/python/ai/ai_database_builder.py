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
from lib.utils import debug, real_lines,get_file_name_from_path,get_line_and_md5_from_file, words,get_sorted_turple_on_dict_by_value
from lib.singleton import Singleton
from lib.loggable import Loggable
from backend.nosql_database import AI_NoSqlDatabase 


class AI_DB_Builder_Constants(object):

    field_word_tag = 'word_tag'
    field_word_tag_map = 'word_tag_map'
    
    field_noun_ys_map = 'noun_ys'

def get_top_n_n_similarity(m,level):
    return _get_top(AI_DB_Builder_Constants.field_noun_ys_map, m, None, level)

def get_top_word_tag(m,nth,level):
    return _get_top(AI_DB_Builder_Constants.field_word_tag_map, m, nth, level)

def _get_top(field_name, m, nth=None, level=1):
    #doing a duck type thing to get the m
    if field_name in m:
        m = m[field_name]
    mm=m[nth] if nth else m
    t = get_sorted_turple_on_dict_by_value(mm,reverse_the_result=True)
    return t[0:level] if level <= len(t) else t


@Singleton
class AIDatabaseBuilder(Loggable):
    _lock_word = threading.RLock()
    _lock_noun_noun_simarility = threading.RLock()
    _db = AI_NoSqlDatabase.Instance()
    #_words_counts_model = None
    #_lock_words_counts_model = threading.RLock()
    
    def __init__(self):
        pass
        #self._db = 
    
    #This is danergous! it should be called with very caution
    def reset_whole_database(self):
        self._db.earse_db()
        self._db.init_database()
    
    #in a sentence wise, len(noun_ys) < a len of a sentence
    def add_noun_nouns_simarility(self, noun_x, noun_ys):
        with self._lock_noun_noun_simarility:
            doc = self.get_noun_similarity(noun_x)
            nn=None
            if doc:
                doc[AI_DB_Builder_Constants.field_noun_ys_map] = self._build_noun_nouns_structure(doc[AI_DB_Builder_Constants.field_noun_ys_map],
                                                                    noun_ys)
                return self._db.update(doc)
            else:
                nys = self._build_noun_nouns_structure(None, noun_ys)
                doc = dict(noun_x=noun_x, noun_ys=nys)
                return self._db.add_to_noun_noun_map(doc)
            
    def add_word_tag(self, word_tag, position_list):
        with self._lock_word:
            doc = self.get_word_tag(word_tag)
            wp=None
            if doc:
                doc[AI_DB_Builder_Constants.field_word_tag_map] = self._build_word_tag_map(doc[AI_DB_Builder_Constants.field_word_tag_map], position_list)
                return self._db.update(doc)
            else:
                wp = self._build_word_tag_map(None, position_list)
                doc = dict(word_tag=word_tag, word_tag_map=wp)
                return self._db.add_to_word_tag_map(doc)
    
    def get_noun_similarity(self, n):
        r = self._db.get_from_noun_noun(n)
        return self._none_if_empty_else_doc(r)
    
    def get_word_tag(self, w):
        r = self._db.get_from_word_tag(w)
        return self._none_if_empty_else_doc(r) 
    
    def _none_if_empty_else_doc(self, o, oo=None):
        if oo:
            return o['doc'][oo] if o else None
        else:
            return o['doc'] if o else None
    
    #position_list: [(1, 'VBZ'), (2, 'DT'), (3, 'NN')], 
    # meaning to add a record with the next word is 'VBZ', the second next word is 'DT' ...etc to the current word, word        
    def _build_word_tag_map(self, existing_word_tag_map, position_list):
        if existing_word_tag_map:
            for p in position_list:
                if p[0] in existing_word_tag_map:
                    pp = existing_word_tag_map[p[0]]
                    if p[1] in pp:
                        pp[p[1]] = pp[p[1]] + 1
                    else:
                        pp[p[1]] = 1
                else:
                    existing_word_tag_map[p[0]] = { p[1]: 1 }
            return existing_word_tag_map
        else:
            d={}
            for p in position_list:
                d[p[0]] = { p[1]: 1 }
            return d
    
    def _build_noun_nouns_structure(self, existing_n_n_structure, noun_ys):
        if existing_n_n_structure:
            for noun_y in noun_ys:
                if noun_y in existing_n_n_structure:
                    existing_n_n_structure[noun_y] = existing_n_n_structure[noun_y] + 1
                else:
                    existing_n_n_structure[noun_y]=1
            return existing_n_n_structure
        else:
            d={}
            for noun_y in noun_ys:
                d[noun_y] = 1
            return d
    
    '''
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
    '''