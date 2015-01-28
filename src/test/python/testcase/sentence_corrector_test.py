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
from ai.sentence_corrector import SentenceCorrector
#from ai.ai_builder import AIBuilder
import unittest
from testcase.utils import build_test_passage

class SentenceCorrectorTest(unittest.TestCase):
    
    _test_resources_base = None
    #_builder = None
    
    def setUp(self):
        #self._builder = AIBuilder.Instance()
        #self._test_resources_base = join(abspath(dirname('__file__')), '../../../resources/ai/test/')
        #self._builder.reset_whole_database()
        #inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test.txt')
        build_test_passage()
        
    
    def test_sentence_suggestions_on_spelling_mistakes(self):
        
        orig_str = 'a maee is stronger than female'
        new_str = SentenceCorrector(orig_str).suggest()
        self.assertEqual(new_str, 'a male is stronger than female')
        
        
        orig_str = 'his decision has been maee'
        new_str = SentenceCorrector(orig_str).suggest()
        self.assertEqual(new_str, 'his decision has been made')
        
        orig_str = 'a male is strangee than female'
        new_str = SentenceCorrector(orig_str).suggest()
        self.assertEqual(new_str, 'a male is stranger than female')
        
        orig_str = 'a male is stranee thzn female'
        new_str = SentenceCorrector(orig_str).suggest()
        self.assertEqual(new_str, 'a male is stranger than female')
    
    def test_sentence_suggestions_on_NO_spelling_mistakes(self):
        orig_str = 'a made is stronger than female'
        new_str = SentenceCorrector(orig_str).suggest()
        self.assertEqual(new_str, 'a male is stronger than female')
        
        