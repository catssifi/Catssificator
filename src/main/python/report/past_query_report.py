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
from lib.utils import debug, convert_to_offset_to_draw, dumps, map_keys_to_the_values,jsonize_str
from backend.database import SQLDatabase,DB_Constants
from backend.category import Category,replace_category_num_with_name

class PastQueryReport(Loggable):
    _offset=None
    _limit=None
    _draw=None
    _ordered_column_index=None
    _ordered_direction=None
    _sqldb=None
    
    #draw parameter is pretty much specify to the datatable web plugin
    def __init__ (self, draw, limit=25, offset=0, ordered_column_index=0, ordered_direction=''):
        self._draw = int(draw)
        self._limit=limit
        self._offset=offset
        self._ordered_column_index=ordered_column_index
        self._ordered_direction=ordered_direction
        self._sqldb=SQLDatabase.Instance()
        
    #returns a json document
    def generate_report(self):
        _cols=[DB_Constants.tbl_Query_Map_col_id, DB_Constants.tbl_Query_Map_col_query, 
               DB_Constants.tbl_Query_Map_col_from_who,
               DB_Constants.tbl_Query_Map_col_categories, DB_Constants.tbl_Query_Map_col_create_date]
        
        #Order by date by default
        if self._ordered_column_index==0:
            self._ordered_column_index=4
            if self._ordered_direction.upper() == 'ASC':
                self._ordered_direction = 'DESC'
            else:
                self._ordered_direction = 'ASC'
        map_results = self._sqldb.select_query_map(cols=_cols, limit=self._limit, offset=self._offset, ordered_column_index=self._ordered_column_index, ordered_direction=self._ordered_direction)
        map_results = map_keys_to_the_values(map_results, _cols)
        map_results = replace_category_num_with_name(map_results, DB_Constants.tbl_Query_Map_col_categories)
        records_total=0 if not map_results else self._sqldb.count_query_map()
        records_filtered=0 if not map_results else records_total
        results={
                    "draw": self._draw, 
                    "recordsTotal": records_total, 
                    "recordsFiltered": records_filtered,
                    "data": 
                             map_results if map_results else [[]]
                    
                 }
        #debug()
        j_response = dumps(results)
        return j_response