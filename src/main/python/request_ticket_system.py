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
from datetime import datetime
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import generate_token
from backend.datastore_factory import DataStoreFactory

@Singleton
class RequestTicketSystem(Loggable):

    _lock = threading.RLock()
    _tickets={}
    _token_len = 40
    
    def __init__(self):
        self._datastore=DataStoreFactory.factory()
    
    def submit(self, ticket_token, category_num):
        (words, time_ticket_created) = (None, None)
        with self._lock:
            (words, time_ticket_created) = self._tickets[ticket_token]
            del self._tickets[ticket_token]
        if words and len(words)>0:
            for word in words:
                self._datastore.store(word, category_num)
    
    def generate_category_ticket(self, words):
        ticket_token= generate_token(self._token_len)
        with self._lock:
            self._tickets[ticket_token] = (words, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return ticket_token