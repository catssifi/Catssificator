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
    
    def get_query_category_suggestions_histogram(self, categories):
        return build_query_category_suggestions_histogram(categories)

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

_category_rank_words=['five', 'four', 'three', 'two', 'one']
def build_query_category_suggestions_histogram(categories_list):
    hist_str='''
          <table style="width:100%" class="table_Histogram">
                <tr >
                    <th>
                        &nbsp;&nbsp;Estimated category distributions:
                    </th>
                </tr>
                <tr>
                  <td>
                  '''
    hist_str+='<div class="histo">'
    animate_str=''
    i=0
    for cat in categories_list:
        rank = get_rank(cat[1]['percentize'])
        hist_str+='<div class="'+rank+' histo-rate">'
        hist_str+='    <span class="histo-star"><i class="active icon-star"></i> '+cat[1]['full-category-name']+' </span>'
        hist_str+='    <span class="bar-block">'
        hist_str+='       <span id="id-bar-'+str(i)+'" class="bar bar-'+rank+'">'
        hist_str+='            <span>'+cat[1]['percentize']+'%</span>&nbsp;'
        hist_str+='       </span>'
        hist_str+='    </span>'
        hist_str+=''
        hist_str+='    '
        hist_str+='</div>'
        
        animate_str+='$("#id-bar-'+str(i)+'").animate({width: "'+cat[1]['percentize']+'%"}, 700); '
        i+=1
    hist_str+='</div>'
    hist_str+='<script>'
    hist_str+='    $(".bar span").hide();'
    hist_str+='    ' + animate_str
    hist_str+='    setTimeout(function() { $(".bar span").fadeIn("slow"); }, 500);'
    hist_str+='</script>'
    
    hist_str+='''</td>
                <td>
                </td>
                </tr>
      </table>'''
    
    return hist_str

def get_rank(percentize):
    percentize=float(percentize)
    if percentize >= 80:
        return _category_rank_words[0]
    if percentize >= 60:
        return _category_rank_words[1]
    if percentize >= 40:
        return _category_rank_words[2]
    if percentize >= 20:
        return _category_rank_words[3]
    
    return _category_rank_words[4]