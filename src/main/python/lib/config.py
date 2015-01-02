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
from yaml import load
from lib.singleton import Singleton
from lib.utils import get_base

@Singleton
class Config():
    
    _mode = ''
    _config_path = get_base('config/setup.yaml') 
    
    def __init__ (self):
        self._mode = self.get_yaml_data(['common', 'run_mode'], 'dev')  
    
    def get_category_path(self):
        if self._mode == 'prod' or self._mode == 'production':
            return 'config/category-production.txt'
        else:
            return 'config/category.txt'
        
    def get_mode(self):
        if not self._mode:
            self.__init__()
        return self._mode
    
    def set_mode(self, m):
        self._mode = m
    
    def set_config_path(self, c_p):
        self._config_path = c_p
    
    def get_config_path(self):
        return self._config_path
    
    def get_yaml_data(self, keys, default=''):
        yaml_file=None
        try:
            yaml_file = open(self.get_config_path(), 'r')
            yaml_obj = load(yaml_file.read())        
            current_tree = yaml_obj
            for key in keys:
                current_tree = current_tree[key]
            result = current_tree
        except Exception as e:
            result = default
        finally:
            if yaml_file:
                yaml_file.close()
        return result