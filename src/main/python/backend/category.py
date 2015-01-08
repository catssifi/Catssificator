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
import operator
from sets import Set
from os.path import abspath, join, dirname
from lib.loggable import Loggable
from lib.singleton import Singleton
from lib.config import Config
from lib.utils import rindex, real_lines, unescape, debug
from backend.database import SQLDatabase
import string

@Singleton
class Category(Loggable):
    _instance = None
    _path = join(abspath(dirname('__file__')), Config.Instance().get_category_path())
    _categoryNameToNum = {}
    _categoryNumToName={}
    _categoryToParentCategory={}    #This is only for production mode (with huge category .txt file)
    _all_root_category_nums={}
    _all_root_category_names={}
    _parent_child_category_nums={}
    _all_category_nums_which_has_childs=Set()
    _ALL_CATEGORIES_DESC=''
    
    def __init__(self):
        self.info('Initializing Category object at path: %s' % (self._path))
        lines = real_lines(self._path)
        if lines:
            lines = map(lambda l: l.replace('\n', ''),lines)
            if Config.Instance().get_mode() == 'prod':
                self.__init_prod(lines)
            else:
                self.__init_dev(lines)
            self.info('Created categoryNameToNum: %s' % (len(self._categoryNameToNum)))
        
    def __init_dev(self, lines):
        i=1
        for line in lines:
            self._categoryNameToNum[line] = i
            self._categoryNumToName[i] = line
            i += 1
    
    # A line would be of format like: Sporting Goods > Water Sports > Swimming > Swim Goggles & Masks
    def __init_prod(self, lines):
        i=1
        previous_processed_category=''
        for line in lines:
            category_at_right_most = rindex(line, '>')
            self._categoryNameToNum[category_at_right_most] = i
            self._categoryNumToName[i] = category_at_right_most
            #Now build the _categoryToParentCategory dictionary
            categories_till_last_arrow = line[:len(line)-len(category_at_right_most)].strip()
            if categories_till_last_arrow :     #if it is not the root category
            	categories_till_last_arrow=categories_till_last_arrow[:len(categories_till_last_arrow)-1].strip()	#remove the trailing '>'
                categories_till_last_arrow=rindex(categories_till_last_arrow, '>')
                tmp=self._categoryNameToNum[categories_till_last_arrow]
                self._categoryToParentCategory[i] = tmp
                if previous_processed_category==categories_till_last_arrow:
                    self._all_category_nums_which_has_childs.add(tmp)
            else:
            	self._categoryToParentCategory[i] = 0
            previous_processed_category=category_at_right_most
            
            #here i am going to save to the sql database
            #SQLDatabase.Instance().insert_into_category(i,category_at_right_most)
            
            i += 1
        self._all_root_category_nums = map((lambda x: x[0]), filter((lambda x: x[1]==0), self._categoryToParentCategory.items()))
        self._all_root_category_names = filter((lambda x: x[0] in self._all_root_category_nums), self._categoryNumToName.items())
    
    
    def get_num(self, name):
        name=unescape(name)
        try:
            return self._categoryNameToNum[name]
        except:
            #Try to see if the name itself is a category number
            if name.isdigit() and int(name) in self._categoryNumToName:
                return int(name)
            else:
                return None
    
    def get_full_name(self, name):
        return self.__get_name_by_name(name, True)
    
    def __get_name_by_name(self, name, full_path=False):
        num=self.get_num(name)
        return self.get_name(num, full_path)
    
    def get_name(self, num, full_path=False):
        str = None
        try:
            num=int(num)
            str=self._categoryNumToName[num]
            if full_path and Config.Instance().get_mode() == 'prod':
                while num in self._categoryToParentCategory:
                    if self._categoryToParentCategory[num] == 0:
                    	break
                    num = self._categoryToParentCategory[num]
                    parent_category=self.get_name(num)
                    str=parent_category+' > '+str
            else:
                pass
        except:
            return None
        return str
        
    def validate(self, category_num):
        return self.get_num(int(category_num))
    
    def is_this_category_num_parent(self, catetory_num):
        return catetory_num in self._all_category_nums_which_has_childs
    
    def suggest_categories(self, q):
        return '{}'
    
    def get_categories_by_name(self, category_name):
    	cat_num = self.get_num(category_name)
    	if cat_num:
    		return self.get_categories(cat_num)
    	else:
    		return None
    
    #If category_num is zero, returns all root level's categories
    def get_categories(self, category_num=0):
        if category_num < 1:
            if Config.Instance().get_mode() == 'prod':
                return self._all_root_category_names
            else:
                return self._categoryNumToName.items()   #returns everything 
        else:
            all_category_nums=self.get_category_nums_from_parent(category_num)
            if all_category_nums:
                all_category_names=filter((lambda x: x[0] in all_category_nums), self._categoryNumToName.items())
                return all_category_names
            else:
                return {}

    def get_category_nums_from_parent(self, parent_category_num):
        #self.debug('get_category_nums_from_parent: %s' % (parent_category_num))
        if parent_category_num in self._parent_child_category_nums:
            return self._parent_child_category_nums[parent_category_num]
        else:
            res = None
            if parent_category_num in self._categoryToParentCategory.values():
                res = map((lambda x: x[0]), filter((lambda x: x[1]==parent_category_num), self._categoryToParentCategory.items()))
            self._parent_child_category_nums[parent_category_num]=res
            return res

    def get_categories_desc(self):
        if not self._ALL_CATEGORIES_DESC :
            s=''
            i=0
            for k in sorted(self._categoryNumToName):
                if i % 3 == 0: 
                    s+='\\n'+'{0: <4}'.format(str(k))+' ' + '{0: <30}'.format(self._categoryNumToName[k])   #double slash is needed because for json 
                else:
                    s+=''+'{0: <4}'.format(str(k))+' ' + '{0: <30}'.format(self._categoryNumToName[k])
                i+=1
            self._ALL_CATEGORIES_DESC=s
        return self._ALL_CATEGORIES_DESC
    
    def set_path(self, new_path):
        self._path=new_path
        self.__init__()

#the dimension of each map_results is hardcored
def replace_category_num_with_name(map_results, category_index):
    category=Category.Instance()
    if map_results:
        for m in map_results:
            m[category_index] = category.get_name(m[category_index]) 
    return map_results
    #debug()
    #i=0
    #for map_result in map_results:
    #    debug()
    #    name=category.get_name(map_result[category_index])
    #    map_results[i][category_index] = name
    #    i+=1
    return new_map_results
    