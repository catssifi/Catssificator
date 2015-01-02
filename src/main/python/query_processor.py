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
import operator

from request_ticket_system import RequestTicketSystem
from backend.datastore_factory import DataStoreFactory
from lib.loggable import Loggable
from lib.utils import stem_all_words, dumps, debug
from backend.category import Category

STOP_WORDS=[u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']

class QueryProcessor(Loggable):
    _datastore = None
    
    def __init__(self, datastore=None):
        if datastore:
            self.info("Setting _datastore to %s " %(str(datastore)))
            self._datastore = datastore
        else:
            self._datastore=DataStoreFactory.factory()
    
    def inquire(self, query):
        words = self.process_query(query);
        category_score = {}
        for word in words:
            word_categories=self._datastore.get(word, with_score=True)
            if word_categories and len(word_categories) > 0:
                for word_category in word_categories:
                    this_category = word_category[0]
                    this_frequency = word_category[1]
                    if this_category in category_score:
                        category_score[this_category] += this_frequency
                    else:
                        category_score[this_category] = this_frequency
        if category_score :
            category_num, value = max(category_score.iteritems(), key=operator.itemgetter(1))
            category_name = Category.Instance().get_name(category_num)
            response_str = dumps({"result":"yes", "category":category_name})
        else:
            ticket_token=RequestTicketSystem.Instance().generate_category_ticket(words)
            message='Unfortunately, no category was found under the search query:%s ...Please pick a category it should belong to: ' % (query)
            message+=Category.Instance().get_categories_desc()
            response_str = dumps({"result":"no", "message":message, "ticket-token":ticket_token})
        return response_str
    
    # parameter: category can be category number or category name
    def submit(self, query, category, dumps_it=True):
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
            for word in words:
                self._datastore.store(word, category_num)
            response_str = {"result":"yes", "message":"query: \'%s\' has been processed!"% (query)}
            if dumps_it:
                response_str = dumps(response_str)
        return response_str
    
    def submit_in_chunk(self, queries, category_num):
        response_str_list=[]
        for query in queries:
            if isinstance(query, list):
                for q in query:
                    response_str_list.append(self.submit(q, category_num, False))
            else:
                response_str_list.append(self.submit(query, category_num, False))
        return dumps(response_str_list)
    
    def process_query(self, query):
        tokenize_words = self.tokenize(query)
        removed_stopwords_words=filter((lambda w: not w in STOP_WORDS), tokenize_words)
        stemmed_words=stem_all_words(removed_stopwords_words)
        return stemmed_words
    
    def tokenize(self, query):
        words = query.split( );
        words = map(lambda x: x.lower().strip(), words)
        return words