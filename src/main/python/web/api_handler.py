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
from lib.utils import dumps, debug, convert_draw_to_offset,remove_non_valid_chars
from backend.fileupload import FileUploader
from report.past_query_report import PastQueryReport

def get_full_name(arguments, from_who=''):
    selected_name=get_argument(arguments, 'selectedName')
    _from_who=from_who
    return Category.Instance().get_full_name(selected_name)

def query(arguments, from_who=''):
    query = get_argument(arguments, 'query')
    _from_who=from_who
    response_str = QueryProcessor().inquire(query)
    return response_str

def submit_query(arguments, from_who=''):
    category_num = get_argument(arguments, 'categoryNum')
    query = get_argument(arguments, 'query')
    token = get_argument(arguments, 'token')
    _from_who=from_who
    response_str = QueryProcessor().submit(query, category_num, token, from_who=_from_who)
    return response_str

def submit_upload(arguments, from_who=''):
    category_num = get_argument(arguments, 'categoryNum')
    tokens_str = get_argument(arguments, 'tokensStr')
    tokens = filter(lambda x: x, tokens_str.split(','))
    queries_lists = FileUploader.retrieve_contents_from_tokens(tokens)
    _from_who=from_who
    response_str = QueryProcessor().submit_in_chunk(queries_lists, category_num, from_who=_from_who)
    FileUploader.remove_tokens(tokens)
    return response_str

def report_past_query(arguments, from_who=''):
    _id = get_argument(arguments, 'id')
    response_str = PastQueryReport(0).generate_detail_report_by_id(_id)
    return response_str
    
def report_past_queries(arguments, from_who=''):
    _draw = get_argument(arguments, 'draw')
    length = get_argument(arguments, 'length')
    _offset=int(get_argument(arguments, 'start')[0])
    _offset=convert_draw_to_offset(_offset, length)
    _ordered_column_index = int(get_argument(arguments, 'order[0][column]')[0])
    _ordered_direction = get_argument(arguments, 'order[0][dir]')
    _from_who=from_who
    response_str = PastQueryReport(limit=length, offset=_offset, draw=_draw, 
                                   ordered_column_index=_ordered_column_index, ordered_direction=_ordered_direction).generate_report()
    return response_str

def suggest_categories(arguments, from_who=''):
    _q = get_argument(arguments, 'query')
    res = Category.Instance().suggest_categories(_q)
    return res

class APIHandler(BaseHandler):
    
    def set_query_cookie(self, arguments):
        query = get_argument(arguments, 'query')
        query = remove_non_valid_chars(query)
        try:
            self.set_cookie(Web_Constans.cookie_Query_name, query)
        except Exception as e:
            self.warn('setting cookie failed: ' + str(e))
    
    def get(self, method):
        response=''
        if method == 'get_full_name':
            response = get_full_name(self.request.arguments, from_who=self.request.remote_ip)
        elif method == 'query': 
            response = query(self.request.arguments, from_who=self.request.remote_ip)
        elif method == 'submit_query': 
            response = submit_query(self.request.arguments, from_who=self.request.remote_ip)
            self.set_query_cookie(self.request.arguments)
        elif method == 'submit_upload': 
            response = submit_upload(self.request.arguments, from_who=self.request.remote_ip)
        elif method == 'report_past_query':
            response = report_past_query(self.request.arguments, from_who=self.request.remote_ip)
        elif method == 'report_past_queries':
            response = report_past_queries(self.request.arguments, from_who=self.request.remote_ip)
        elif method == 'suggest_categories':
            response = suggest_categories(self.request.arguments, from_who=self.request.remote_ip)
        self.write(response)

class Web_Constans(object):
    cookie_NAME_SPACE='catssificator_cookie_'
    cookie_Query_name = cookie_NAME_SPACE +'query'
    