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
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), './src/main/python/'))

from lib.utils import debug,get_files_only_from_dir
from lib.loggable import Loggable
from ai.ai_builder import AIBuilder
from ai.new_vocab_collections import NewVocabCollections
import argparse

class AIDataImporter(Loggable):
	
	_content_locatoin = None
	_builder = None
	
	def __init__(self, content_locatoin):
		self._content_locatoin=join(abspath(dirname('__file__')), content_locatoin)
		self._builder = AIBuilder.Instance()
	
	def process(self):
		files = get_files_only_from_dir(self._content_locatoin)
		for file in files:
			inserted = self._builder.add_build_from_file(self._content_locatoin+file)
			self.info('Num of inserted: %s'%(inserted))

#For now, just manually import the new vocab
nc = NewVocabCollections.Instance()
nc.add('IPhone')

	
#The program starts here
parser = argparse.ArgumentParser(description='Import the text/url data to the AI database')
parser.add_argument('location', help='It can be a dir or file or url')
args = parser.parse_args()
content_locatoin = args.location
	
if __name__ == '__main__':
	ai_importer = AIDataImporter(content_locatoin)
	ai_importer.process()
