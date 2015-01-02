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
from web.uibuilder import UIBuilder
from web.base_handler import BaseHandler

class HomePageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        #_category_menu_in_html = UIBuilder.Instance().get_category_menu()
        self.render("index.html")

class UploadPageHandler(BaseHandler):
    def get(self):
        #self.write("Hello, world")
        _category_menu_in_html = UIBuilder.Instance().get_category_menu()
        self.render("upload.html", categories=_category_menu_in_html)