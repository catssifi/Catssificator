#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from backend.fileupload import FileUploader
from lib.config import Config
from lib.utils import is_path_exist, debug
from query_processor import QueryProcessor
import unittest

class FileUploadTestHelper():
	
	@staticmethod
	def create_fileupload_test_object_and_store(file_upload_path, file_name, content):
		file_up = FileUploader(file_name, content)
		file_up.set_file_upload_base_dir(file_upload_path)
		file_up.store()
		return file_up

class FileUploadTest(unittest.TestCase):

	_test_dir=join(abspath(dirname('__file__')), '../../../config/test/')
	_file_upload_path = None

	def setUp(self):
		config_file = self._test_dir + 'setup-test.yaml'
		Config.Instance().set_config_path(config_file)
		self._file_upload_path = Config.Instance().get_yaml_data(['common', 'file_upload_base_dir'], '/tmp/catssificator-upload-test')
	
	def test_file_upload(self):
		file_upload = FileUploadTestHelper.create_fileupload_test_object_and_store(self._file_upload_path, 'hello.txt', 'wei i am okay...But i am not sure about you!..& okay?')
		uploaded_sucess= False
		uploaded_path = file_upload.get_uploaded_path()
		if uploaded_path and is_path_exist(uploaded_path):
			uploaded_sucess = True
		self.assertEqual(uploaded_sucess, True)
		deleted_sucess=False
		#debug()
		file_upload.remove()
		if uploaded_path and not is_path_exist(uploaded_path):
			deleted_sucess=True
		self.assertEqual(deleted_sucess, True)
	
	def test_files_upload_and_retrieve_and_remove_and_submit(self):
		file_upload_1 = FileUploadTestHelper.create_fileupload_test_object_and_store(self._file_upload_path, 'test-2a.txt', 'this is the first second test 2...OKay?')
		file_upload_2 = FileUploadTestHelper.create_fileupload_test_object_and_store(self._file_upload_path, 'test-2b.txt', 'The Galaxy S 5 Mini features a heart rate monitor and together with the S Health™ app, it makes tracking your health and fitness goals a lot easier. You can also use S Health to get on-demand nutritional information and the built-in pedometer helps track your steps and calories burned...')
		file_upload_3 = FileUploadTestHelper.create_fileupload_test_object_and_store(self._file_upload_path, 'test-2c.txt', 'this is the third  test...OKay?')
		tokens = []
		tokens.append(file_upload_1.get_token())
		tokens.append(file_upload_2.get_token())
		tokens.append(file_upload_3.get_token())
		queries = FileUploader.retrieve_contents_from_tokens(tokens)
		self.assertNotEqual(queries, None)
		FileUploader.remove_tokens(tokens)
		
		#Now i submitted it to the QueryProcessor()
		response_str = QueryProcessor().submit_in_chunk(queries, "1")
		#debug()
		self.assertNotEqual(queries, None)
		
		
		