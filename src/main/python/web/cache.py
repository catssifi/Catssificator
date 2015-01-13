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

import os
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.utils import debug, convert_datetime_to_s,add_seconds_to_datetime
from lib.config import Config
from datetime import datetime
from backend.database import SQLDatabase

time_since_restarted = convert_datetime_to_s(datetime.now()) + '+00:00 '+ os.environ['TZ']

def get_server_time_since_last_restarted():
        return time_since_restarted

class Cache_Field(object):
    submissions_today = 'submissions_today'
    submissions_in_the_past_n_days = 'submissions_in_the_past_n_days'

@Singleton
class Cache(Loggable):
    
    _sqldb = SQLDatabase.Instance();
    _config = Config.Instance()
    _cache = {}
    _submissions_today_expir_cycle = None
    _submissions_in_the_past_n_days_expir_cycle = None
    _yaml_section = 'cache'
    
    def __init__(self):
        self._submissions_today_expir_cycle = Config.Instance().get_yaml_data([self._yaml_section, Cache_Field.submissions_today])
        self._submissions_in_the_past_n_days_expir_cycle = Config.Instance().get_yaml_data([self._yaml_section, Cache_Field.submissions_in_the_past_n_days])
        self.info('At Cache constructor...._submissions_today_expir_cycle: '+ self._submissions_today_expir_cycle)
    
    def get_submissions_today(self, refresh=False):
        count = self._retrieve_from_cache(Cache_Field.submissions_today, self._submissions_today_expir_cycle)
        if not count or refresh:
             count = self._sqldb.get_aggregate_submission_count()   #call the corresponding underlying function
             #self.info('refreshing from the cache on submissions_today: ' + count)
             self._update_cache(Cache_Field.submissions_today, count)     #also update the cache layer
        return count
    
    def get_submissions_in_the_past_n_days(self, back_days, refresh=False):
        field_name=Cache_Field.submissions_in_the_past_n_days+'_'+str(back_days)
        count = self._retrieve_from_cache(field_name, self._submissions_in_the_past_n_days_expir_cycle)
        if not count or refresh:
            count = self._sqldb.get_aggregate_submission_count(back_days=back_days)
            self.info('refreshing from the cache on submissions_in_the_past_%s_days: %s'%(str(back_days),count))
            self._update_cache(field_name, count)     #also update the cache layer
        return count
    
    def _retrieve_from_cache(self, field_name, interval_in_seconds):
        if field_name in self._cache:
            entry_created_time = self._cache[field_name][0]
            entry_adjusted_time = add_seconds_to_datetime(entry_created_time, interval_in_seconds)
            if entry_adjusted_time > datetime.now():
                return self._cache[field_name][1]   #returns the value if it is still within the range
        return None #else returns nothing
    
    def _update_cache(self, field_name, value):
        self._cache[field_name] = (datetime.now(), value)   #simply update the cache
