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

from backend.category import Category
from lib.singleton import Singleton
from lib.utils import debug
'''
This class is to build all the web UI components and return the html code in each individual method
'''
@Singleton
class UIBuilder():
    
    _category_menu_in_html = None
    
    def __init__(self):
        self._category_menu_in_html = build_category_menu()
        
    def get_category_menu(self):
        return self._category_menu_in_html

def build_category_menu(category_num=None):
    
    categories=None
    str=''
    #debug()
    if category_num:
        categories = Category.Instance().get_categories(category_num)
        str='<ul>'
        if not categories:
        	return None
    else:
        categories = Category.Instance().get_categories()
        str='<ul id="category_menu">'
    
    sub_categories = None
    for category in categories:
        if Category.Instance().is_this_category_num_parent(category[0]):
            sub_categories=build_category_menu(category[0])
            #if sub_categories:
            str+=('<li select-able="false" cat-num="%s">'+category[1])%(category[0])
            str+=sub_categories
        else:
            str+=('<li select-able="true" cat-num="%s">'+category[1])%(category[0])
        str+='</li>'
    str+='</ul>'
    
    #_category_menu = str
    return str