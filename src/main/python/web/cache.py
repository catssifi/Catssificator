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

from lib.loggable import Loggable;
from lib.singleton import Singleton
from lib.utils import debug
from backend.database import SQLDatabase


@Singleton
class Cache(Loggable):
    
    _sqldb = SQLDatabase.Instance();
    
    def get_submissions_today(self):
        count = self._sqldb.get_aggregate_submission_count()
        return count
    
    def get_submissions_in_the_past_n_days(self, back_days):
        count = self._sqldb.get_aggregate_submission_count(back_days=back_days)
        return count
        