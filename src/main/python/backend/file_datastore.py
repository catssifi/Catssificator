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
import shelve
import exceptions
from datastore import DataStore
from lib.loggable import Loggable
from lib.utils import is_string, stem_word, get_base, debug

class FileDataStore(DataStore):
    _filename = get_base('data/backend')
    
    def __init__(self, file_name=None):
        if file_name:
            self._filename = file_name
        #self.info("Setting the filename: %s" % self._filename)
    
    def store(self, word, *args_category_num, **kwargs_category_num):
        d = shelve.open(self._filename, writeback=True)
        try:
            stemmed_word = stem_word(word)
            if d and stemmed_word in d:
                dd = d[stemmed_word]
            else:
                dd = {}
                d[stemmed_word] = dd
                
            for cat_num in args_category_num:
                cat_num = int(cat_num) if is_string(cat_num) else cat_num
                if cat_num in dd :
                    dd[cat_num] += 1
                else:
                    dd[cat_num] = 1
        finally:
            d.close()
            
        #self.info("Storing %s" % len(args_category_num))
        
    def get_by_word_only(self, word):
        try:
            d = shelve.open(self._filename)
        except:
            self.error("dictionary failed to open...")
            return None
        stemmed_word = stem_word(word)
        if d and stemmed_word in d:
            s = d[stemmed_word]
            d.close()
            return s
        else:
            return None
    
    def get(self, word, category_num=None, with_score=False):
        categories = self.get_by_word_only(word) 
        if categories:
            if category_num and category_num in categories:
                return categories[category_num]
            else:
                #returns the category_num with highest score
                results=self.get_categories_with_n_highest_score(categories)
                if with_score:
                    return results
                else:
                    return map(lambda r: r[0], results)
        else:
            return None
    
        