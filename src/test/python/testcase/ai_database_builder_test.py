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
from lib.utils import debug
from ai.ai_database_builder import AIDatabaseBuilder
import unittest


class AIDatabaseBuilderTest(unittest.TestCase):
    
    _test_resources_base = None
    _builder = None
    
    def setUp(self):
        self._builder = AIDatabaseBuilder.Instance()
        self._test_resources_base = join(abspath(dirname('__file__')), '../../../resources/ai/test/')
        self._builder.reset_whole_database()
    
    def test_build_word_counts_and_load(self):
        len_of_model=586
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test.txt')
        self.assertEqual(inserted, len_of_model)
        
        #Try to insert it again and it should return nothing
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test.txt')
        self.assertEqual(inserted, None)
        
        #Now try to load it back to the memory from the database
        model = self._builder.load_words_counts_model()
        self.assertEqual(len(model), len_of_model)
        self.assertEqual(model['the'], 64)
        
        #Now insert the second file
        len_of_model=686
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test_2.txt')
        self.assertEqual(inserted, len_of_model)
        model = self._builder.load_words_counts_model()
        self.assertEqual(model['the'], 443)
        
        self._builder.reset_whole_database()
        
        model = self._builder.load_words_counts_model()
        self.assertEqual(len(model), 0)
        
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test_2.txt')
        model = self._builder.load_words_counts_model()
        self.assertEqual(model['the'], 379) #it should be 443 - 64
        
        
        