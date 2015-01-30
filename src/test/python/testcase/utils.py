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

#THIS UTILS FILE IS FOR UNIT TESTS ONLY

def build_test_passage():
	b = AIBuilder.Instance() 
	
	b.process_message('A decision is made about you, and you have no idea why it was done')
	b.process_message('I made a good decision always!')
	b.process_message('good decision is always hard to make!')
	b.process_message('supported and posted by the non-profit Wikimedia Foundation!')
	
	b.process_message('A male cannot reproduce sexually without access to at least one ovum from a female, but some organisms can reproduce both sexually and asexually.')
