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
import string
from web.base_handler import BaseHandler, get_argument
from backend.category import Category
from backend.fileupload import FileUploader
from query_processor import QueryProcessor
from lib.utils import dumps, get_json_value, get_httpfile, debug

class FileUploadHandler(BaseHandler):

	def post(self):
		results=[]
		for httpfile in self.request.files['files[]']:	
			body = get_httpfile(httpfile, 'body')
			filename = get_httpfile(httpfile, 'filename')
			file_upload = FileUploader(filename, body)
			file_upload.store()		#do the actual upload and store into the server
			file_url = file_upload.get_uploaded_relative_url()
			if file_url:
				file_size = self.request.headers['Content-Length']
				thumb_url = '/thumb_url'
				file_delete_url = '/uploaddelete/'+file_url
				results.append({"name":filename, 
	                       "size":file_size, 
	                       "token": file_upload.get_token(),
	                       "url":file_url, 
	                       "thumbnail_url":thumb_url,
	                       "delete_url":file_delete_url, 
	                       "delete_type":"POST",})
			else:
				results.append({"name":filename, 
	                       "size":file_size, 
	                       "error":file_upload.get_error_msg()})
		results = {"files": results}
		j_response = dumps(results)
		self.write(j_response)