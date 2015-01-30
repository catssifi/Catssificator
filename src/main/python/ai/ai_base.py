#!/usr/bin/python
# Copyright (c) 2015 Ken Wu
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
from lib.utils import get_sorted_turple_on_dict_by_value
from lib.loggable import Loggable
from backend.nosql_database import AI_NoSqlDatabase

class AI_DB_Constants(object):

    field_word_tag = 'word_tag'
    field_word_tag_map = 'word_tag_map'
    
    field_noun_ys_map = 'noun_ys'
    
    #This is for index: NOSQL_DB_Constants.tbl_Processed_File
    field_md5 = 'md5'
    field_file_path = 'file_path'
    field_processed_date = 'processed_date'

def _get_top(field_name, m, nth=None, level=1):
    #doing a duck type thing to get the m
    if not m:
        return None
    if field_name in m:
        m = m[field_name]
    mm= (m[nth] if nth in m else None) if nth else m
    if mm:
        t = get_sorted_turple_on_dict_by_value(mm,reverse_the_result=True)
        return t[0:level] if level <= len(t) else t
    else:
        return None


class AIBase(Loggable):

    _lock_word = threading.RLock()
    _lock_noun_noun_simarility = threading.RLock()
    _db = AI_NoSqlDatabase.Instance()
    