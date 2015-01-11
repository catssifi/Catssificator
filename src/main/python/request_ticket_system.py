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

import threading
import string
from datetime import datetime, timedelta
from collections import OrderedDict
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import generate_token, debug,divide_a_by_b
from backend.datastore_factory import DataStoreFactory

@Singleton
class RequestTicketSystem(Loggable):

    _lock = threading.RLock()
    _tickets=OrderedDict()
    _token_len = 40
    
    _num_of_items_to_clean_each_loop = 50
    _seconds_backward=3*60*60   #3 hours
    
    def __init__(self):
        self._datastore=DataStoreFactory.factory()
    
    def submit(self, ticket_token, category_num):
        (query, words, time_ticket_created) = (None, None, None)
        with self._lock:
            (query, words, time_ticket_created) = self._tickets[ticket_token]
            del self._tickets[ticket_token]
        len_words=len(words)
        word_strength=divide_a_by_b(1, len_words)
        if words and len_words>0:
            for word in words:
                self._datastore.store(word, word_strength, [category_num])
    
    def generate_category_ticket(self, query, words):
        ticket_token= generate_token(self._token_len)
        with self._lock:
            self._tickets[ticket_token] = (query, words, datetime.now())
        return ticket_token
    
    def get_query(self, token):
        (query, words, time_ticket_created) = (None, None, None)
        with self._lock:
            if token in self._tickets:
                (query, words, time_ticket_created) = self._tickets[token]
        return query
    
    def get_words(self, token):
        (query, words, time_ticket_created) = (None, None, None)
        with self._lock:
            (query, words, time_ticket_created) = self._tickets[token]
        return words
    
    def remove(self, token):
        with self._lock:
            if token in self._tickets:
                del self._tickets[ticket_token]
    
    def set_seconds_backward_for_clean_up(self, sec):
        self._seconds_backward = sec
    
    def size(self):
        return len(self._tickets)
    
    def clean_up(self):
        start_time=datetime.now()
        clean_time_up_to = start_time - timedelta(seconds=self._seconds_backward)
        deleted=0
        #debug()
        with self._lock:
            for k, v in self._tickets.items():
                that_time = v[2]
                if clean_time_up_to > that_time or deleted>self._num_of_items_to_clean_each_loop:
                    break
                else:
                    del self._tickets[k]
                    deleted+=1
        end_time=datetime.now()
        time_taken_str = str(end_time-start_time)
        current_size=self.size()
        self.info("Removed %s tokens in %s seconds ( %s tokens remained)"%(deleted,time_taken_str, current_size))