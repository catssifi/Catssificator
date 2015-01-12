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
import operator

from request_ticket_system import RequestTicketSystem
from backend.datastore_factory import DataStoreFactory
from lib.loggable import Loggable
from lib.utils import stem_all_words,dumps,debug,extract_head_tail,get_all_stop_words,get_sorted_turple_on_dict_by_value,get_percentize, enclose_tag,divide_a_by_b
from backend.category import Category
from backend.database import SQLDatabase
from web.constants import JSON_API_Constants

class QueryProcessor(Loggable):
    _datastore = None
    
    def __init__(self, datastore=None):
        if datastore:
            self.info("Setting _datastore to %s " %(str(datastore)))
            self._datastore = datastore
        else:
            self._datastore=DataStoreFactory.factory()
    
    def inquire(self, query, return_full_categories_if_not_found=False):
        words = self.process_query(query);
        category_score = {}
        response_obj={}
        for word in words:
            word_categories=self._datastore.get(word, with_score=True)
            if word_categories and len(word_categories) > 0:
                for word_category in word_categories.items():
                    this_category = word_category[0]
                    this_frequency = word_category[1]
                    if this_category in category_score:
                        category_score[this_category] += this_frequency
                    else:
                        category_score[this_category] = this_frequency
        if category_score :
            category_num, value = max(category_score.iteritems(), key=operator.itemgetter(1))
            category_name = Category.Instance().get_name(category_num)
            category_full_name = Category.Instance().get_full_name(category_num)
            message = 'The query \'<b>%s</b>\' most likely belongs to: \'<b>%s</b>\'' %(extract_head_tail(query), category_name)
            message = enclose_tag(message, 'h3')
            category_score_list = self.convert_to_histogram_obj(category_score)
            response_obj = {"result":"yes", "category":category_name, "category-full-name": category_full_name, "message": message
                            , JSON_API_Constants.query_category_histogram: category_score_list}
        else:
            message='Unfortunately, no category was found under the search query:%s ...' % (query)
            ticket_token=RequestTicketSystem.Instance().generate_category_ticket(query, words)
            if return_full_categories_if_not_found:
                message+='Please pick a category it should belong to: ' + Category.Instance().get_categories_desc()
            response_obj = {"result":"no", "message":message, "ticket-token":ticket_token}
        return response_obj
    
    # parameter: category can be category number or category name
    def submit(self, query, category, dumps_it=True, token=None, from_who=''):
        if not category.isdigit():
            category_num = Category.Instance().get_num(category)
        else:
            category_num = Category.Instance().validate(category)
        
        response_str=None
        if not category_num:
            response_str = {"result":"no", "message":"invalid category: %s"% category}
            if dumps_it:
                response_str = dumps(response_str)
        else:
            words = self.process_query(query);
            len_words=len(words)
            word_strength=divide_a_by_b(1, len_words)
            for word in words:
                self._datastore.store(word, word_strength, [category_num]) #store it to the in-memory store
            response_str = {"result":"yes", "message":"query: \'%s\' has been processed!"% (extract_head_tail(query))}
            if dumps_it:
                response_str = dumps(response_str)
            
            #also clean up this token:
            if token:
                RequestTicketSystem.Instance().remove(token)
            
            #record the query with category to the long term storage
            SQLDatabase.Instance().insert_into_query_map(query, from_who, str(category_num))
            
            #increment the submission count
            SQLDatabase.Instance().increment_submission_count()
            
        return response_str
    
    def submit_in_chunk(self, queries_lists, category_num, from_who=''):
        response_str_list=[]
        for queries in queries_lists:
            response_str_list.append(self.submit(queries, category_num, False, from_who=from_who))
        return dumps(response_str_list)
    
    def process_query(self, query):
        tokenize_words = self.tokenize(query)
        removed_stopwords_words=filter((lambda w: not w in get_all_stop_words()), tokenize_words)
        stemmed_words=stem_all_words(removed_stopwords_words)
        return stemmed_words
    
    def tokenize(self, query):
        words = query.split( );
        words = map(lambda x: x.lower().strip(), words)
        return words
    
    def convert_to_histogram_obj(self, category_score):
        sorted_category_score=get_sorted_turple_on_dict_by_value(category_score, reverse_the_result=True)
        total_score=category_score.values()[0]
        if len(category_score) > 1:
            total_score=0.0
            for cccc in category_score.items():
                total_score+=cccc[1]
            #total_score=reduce(lambda x, y: x[1] + y[1], category_score)
        new_category_score={}
        new_category_score_list=list()
        for c_s in sorted_category_score:
            percentize = get_percentize(c_s[1], total_score)
            new_category_score = (c_s[0], { "percentize": str(percentize), "full-category-name": Category.Instance().get_full_name(c_s[0])})
            new_category_score_list.append(new_category_score)
        return new_category_score_list
        
        