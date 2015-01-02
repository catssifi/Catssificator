#!/usr/bin/python
# Copyright (c) 2014-2015 Ken Wu
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


from file_datastore import FileDataStore
from lib.loggable import Loggable

class DataStoreFactory(Loggable):
    # Create based on class name:
    def factory(type=''):
        #return eval(type + "()")
        if type=='' or type == "FileDataStore":
            fds = FileDataStore()
            fds.set_retrieve_categories_level(3)
            return fds
        else:   return None
        
    factory = staticmethod(factory)