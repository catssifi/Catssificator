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
from ai.ai_database_builder import AIDatabaseBuilder
import unittest


class SentenceCorrectorTest(unittest.TestCase):
    
    _test_resources_base = None
    _builder = None
    
    def setUp(self):
        self._builder = AIDatabaseBuilder.Instance()
        self._test_resources_base = join(abspath(dirname('__file__')), '../../../resources/ai/test/')
        self._builder.reset_whole_database()
        inserted = self._builder.add_build_from_file(self._test_resources_base+'BigTextForAiDatabase-test.txt')
        
    
    def test_sentence_suggestions(self):
        orig_str='wher is the place'
        corrector = SentenceCorrector(orig_str)
        
        #debug()
        new_str=corrector.suggest()
        #self.assertEqual(new_str, 'where is the place')
        self.assertEqual(new_str, 'hello')
        