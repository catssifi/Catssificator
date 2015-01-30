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
from ai.ai_builder import AIBuilder
from ai.ai_reader import AIReader,WORD_TYPE
from testcase.utils import build_test_passage
import unittest


class AIBuilderReaderTest(unittest.TestCase):
    
    _test_resources_base = None
    _builder = None
    _reader = None
    
    def setUp(self):
        self._builder = AIBuilder.Instance()
        self._test_resources_base = join(abspath(dirname('__file__')), '../../../resources/test/ai/')
        self._builder.reset_whole_database()
        self._reader = AIReader.Instance()
        
    
    def prepare_fake_word_map(self, builder, first_word_tag):
        b=builder
        
        b.add_word_tag([(1,first_word_tag), (2, 'VBZ'), (3, 'DT'),    (4, 'NN')])
        b.add_word_tag([(1,first_word_tag), (2, 'VBZ'), (3, 'JJ'),    (4, 'NN')])
        b.add_word_tag([(1,first_word_tag), (2, 'DT'),  (3, 'VBZ'),   (4, 'JJ')])
        b.add_word_tag([(1,first_word_tag), (2, 'DT'),  (3, 'VBZ'),   (4, 'JJ'), (5, 'VBZ')])
        b.add_word_tag([(1,first_word_tag), (2, 'DT'),  (3, 'VBZ'),   (4, 'NNS'), (5, 'VBZ')])
        b.add_word_tag([(1,first_word_tag), (2, 'DT'),  (3, 'DT'),   (4, 'NN'), (5, 'VBZ')])   
        
    def test_build_word_map(self):
        
        first_word_tag='NN'
        self.prepare_fake_word_map(self._builder, first_word_tag)
        #self.assertNotEqual(results,None)
        
        r=self._reader
        results = r.get_top_word_tag(first_word_tag, 2, 2)
        self.assertEqual(results[0][0], 'VBZ')
        
        #now try with level=100, it should just return all elements in the map
        results = r.get_top_word_tag(first_word_tag, 2, 100)
        self.assertEqual(len(results), 3)
        
        results = r.get_top_word_tag(first_word_tag, 4, 1)
        self.assertEqual(results[0][0], 'VBZ')
        
    '''
    def test_build_noun_noun_similarity(self):
        
        b = self._builder
        w_python='python'
        debug()
        b.add_noun_noun_simarility([w_python, 'programming', 'tools', 'kit'])
        b.add_noun_noun_simarility([w_python, 'scale', 'programming', 'implementations', 'tools'])
        b.add_noun_noun_simarility([w_python, 'language', 'programming', 'tools'])
        b.add_noun_noun_simarility([w_python, 'language', 'programming'])
        b.add_noun_noun_simarility([w_python, 'language', 'tools'])
        b.add_noun_noun_simarility([w_python, 'programming'])
        
        r=self._reader
        results = r.get_top_noun_similarity(w_python,2)
        self.assertEqual(results[0][0], 'programming')
        self.assertEqual(results[1][0], 'tools')
        
        #Now doing the reverse side loook back
        w_tools='tools'
        results = r.get_top_noun_similarity(w_tools,2)
        self.assertEqual(results[0][0], 'python')
        self.assertEqual(results[1][0], 'programming')
        '''
            
    def test_process_sentence(self):
        
        build_test_passage()
        
        w_decision='decision'
        r=self._reader
        results = r.get_top_noun_similarity(w_decision,2, WORD_TYPE().ADJ)
        self.assertEqual(results[0][0], 'good')
        
    def test_import_file(self):
        #debug()
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test_1.txt')
        self.assertNotEqual(inserted, None)
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test_2.txt') 
        self.assertNotEqual(inserted, None) #make sure nothing being inserted again
        
        r=self._reader
        results=r.get_top_noun_similarity('Majesty', 3)
        #debug()
        self.assertEqual(results[0][0], 'condescend') #letters should appear the most with the word Majesty
        
        
        #self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test_2.txt')
        #debug()
        #results=r.get_top_noun_similarity('query', 3) 
        #self.assertEqual(results, None) #make sure nothing being inserted again
        
        '''
        #Try to insert it again and it should return nothing
        
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
        '''
        
        