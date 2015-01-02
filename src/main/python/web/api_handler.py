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
from query_processor import QueryProcessor
from lib.utils import dumps
from backend.fileupload import FileUploader

def get_full_name(arguments):
    selected_name=get_argument(arguments, 'selectedName')
    return Category.Instance().get_full_name(selected_name)

def query(arguments):
    query = get_argument(arguments, 'query')
    response_str = QueryProcessor().inquire(query)
    return response_str

def submit_query(arguments):
    category_num = get_argument(arguments, 'categoryNum')
    query = get_argument(arguments, 'query')
    response_str = QueryProcessor().submit(query, category_num)
    return response_str

def submit_upload(arguments):
    category_num = get_argument(arguments, 'categoryNum')
    tokens_str = get_argument(arguments, 'tokensStr')
    tokens = filter(lambda x: x, tokens_str.split(','))
    queries = FileUploader.retrieve_contents_from_tokens(tokens)
    response_str = QueryProcessor().submit_in_chunk(queries, category_num)
    FileUploader.remove_tokens(tokens)
    return response_str

class APIHandler(BaseHandler):
    def get(self, method):
        response=''
        if method == 'get_full_name':
            response = get_full_name(self.request.arguments)
        elif method == 'query': 
            response = query(self.request.arguments)
        elif method == 'submit_query': 
            response = submit_query(self.request.arguments)
        elif method == 'submit_upload': 
            response = submit_upload(self.request.arguments)
        self.write(response)
    