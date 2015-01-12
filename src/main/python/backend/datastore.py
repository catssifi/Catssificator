#!/usr/bin/python
# Copyright (c) 2014-2015 Ken Wu
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


from abc import ABCMeta, abstractmethod
from lib.loggable import Loggable
from lib.utils import get_categories_with_n_highest_score

class DataStore(Loggable):
    __metaclass__ = ABCMeta
    _retrieve_categories_level=1
    
    #count_score is float number between 0.0 to 1.0
    @abstractmethod
    def store(self, word, count_score=1.0, category_nums=[]):
        pass
    
    #If category_num is None, then returns the category_num(s) by the word
    #If with_score is set to true, then highest score(s) will be returned with its associated category_num
    @abstractmethod
    def get(self, word, category_num=None, with_score=False):
        pass
    
    def get_categories_with_n_highest_score(self, categories):
        return get_categories_with_n_highest_score(categories,self._retrieve_categories_level)
    
    def set_retrieve_categories_level(self, n):
        self._retrieve_categories_level=n
