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

from lib.loggable import Loggable
from lib.utils import debug, convert_to_offset_to_draw, dumps
from backend.database import SQLDatabase,DB_Constants

class PastQueryReport(Loggable):
    _offset=None
    _limit=None
    _sqldb=None
    
    def __init__ (self, limit=25, offset=0):
        self._limit=limit
        self._offset=offset
        self._sqldb=SQLDatabase.Instance()
        
    #returns a json document
    def generate_report(self):
        _cols=[DB_Constants.tbl_Query_Map_col_id, DB_Constants.tbl_Query_Map_col_query, 
               DB_Constants.tbl_Query_Map_col_from_who,
               DB_Constants.tbl_Query_Map_col_categories, DB_Constants.tbl_Query_Map_col_create_date]
        map_results = self._sqldb.select_query_map(cols=_cols, limit=self._limit, offset=self._offset)
        records_total=0 if not map_results else self._sqldb.count_query_map()
        records_filtered=0 if not map_results else records_total
        results={
                    "draw": convert_to_offset_to_draw(self._offset, self._limit), 
                    "recordsTotal": records_total, 
                    "recordsFiltered": records_filtered,
                    "data": 
                             map_results if map_results else [[]]
                    
                 }
        j_response = dumps(results)
        return j_response