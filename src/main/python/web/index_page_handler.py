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
from lib.utils import debug,convert_datetime_to_s
from web.uibuilder import UIBuilder
from web.base_handler import BaseHandler, get_argument
from web.cache import Cache
from request_ticket_system import RequestTicketSystem
from datetime import datetime

class HomePageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        #_category_menu_in_html = UIBuilder.Instance().get_category_menu()
        self.render("index.html")

class UploadPageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        #debug()
        _category_menu_in_html = UIBuilder.Instance().get_category_menu()
        _token=get_argument(self.request.arguments, 'token')
        _query=None
        if _token:
            _query=RequestTicketSystem.Instance().get_query(_token)
        self.render("upload.html", categories=_category_menu_in_html, token=_token, query=_query)
        
class ReportsPageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        #debug()
        _submissions_today = Cache.Instance().get_submissions_today()
        _submissions_in_the_past_7_days = Cache.Instance().get_submissions_in_the_past_n_days(7)
        _submissions_in_the_past_30_days = Cache.Instance().get_submissions_in_the_past_n_days(30)
        now= datetime.now()
        _year=now.year
        _month=now.month
        _day=now.day
        _hour=now.hour
        _minute=now.minute
        _second=now.second
        
        self.render("reports.html", submissions_today=_submissions_today
                    , submissions_in_the_past_7_days=_submissions_in_the_past_7_days
                    , submissions_in_the_past_30_days=_submissions_in_the_past_30_days
                    , year=_year, month=_month, day=_day, hour=_hour, minute=_minute, second=_second)
        
class AboutPageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        #debug()
        _category_menu_in_html = UIBuilder.Instance().get_category_menu()
        self.render("about.html")
    
class ChangesPageHandler(BaseHandler):
    def get(self):
        _referer = self.request.headers['referer']
        self.render("changes.html", referer=_referer)