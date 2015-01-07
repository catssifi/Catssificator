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

from os.path import abspath, join, dirname
from lib.config import Config
from lib.loggable import Loggable 
from lib.utils import generate_token, ensure_dir_exists, del_dir, read_contents_from_dir, debug

class FileUploader(Loggable):
    
    _file_name = None
    _file_content = None
    _upload_path = None
    _upload_path_with_file_name = None
    __file_upload_base_dir = Config.Instance().get_yaml_data(['common', 'file_upload_base_dir'], '/upload')
    _file_upload_base_dir = __file_upload_base_dir
    _file_upload_base_relative_dir = __file_upload_base_dir
    _token = None
    _token_len = 30
    _sucess = False
    _started = False
    _deleted = False
    _error_msg = ''
    
    def __init__ (self, file_name, file_content):
        self._file_name = file_name
        self._file_content = file_content
        self._file_upload_base_dir = FileUploader.__pathify(self._file_upload_base_dir)
    
    @staticmethod
    def __pathify(pp):
        if pp[0] == '/':
            return pp
        p = join(abspath(dirname('__file__')), './data/')
        ppp=p+pp
        return ppp
    
    def set_file_upload_base_dir(self, path):
        path = FileUploader.__pathify(path)
        FileUploader.__file_upload_base_dir = path
        self._file_upload_base_dir = path
    
    def store (self):
        self._started = True
        self._token = generate_token(self._token_len)
        ensure_dir_exists(self._file_upload_base_dir)
        self._upload_path = self._file_upload_base_dir + '/' + self._token
        ensure_dir_exists(self._upload_path)
        self._upload_path_with_file_name = self._upload_path + '/' + self._file_name
        try:
            file_handler = open(self._upload_path_with_file_name, 'w')
            file_handler.write(self._file_content)
            file_handler.close()
            self._sucess = True
        except Exception as e:
            self.error('Writing file: %s failed with reason: %s'%(self._file_name, str(e)))
            self._error_msg = str(e)
    
    def get_error_msg(self):
        return self._error_msg
    
    def get_token(self):
        return self._token
    
    def is_upload_sucess(self):
        return self._sucess
    
    
    def get_uploaded_path(self):
        if self._sucess:
            return self._upload_path_with_file_name
        else:
            return None
    
    def get_uploaded_relative_url(self):
        if self._sucess:
            return '/data/' + self._file_upload_base_relative_dir + '/' + self._token + '/' + self._file_name
        else:
            return None
    
    def remove(self):
        FileUploader.remove_upload(self._token)
        self._deleted=True
        
    @staticmethod
    def remove_upload(token):
    	base_path = FileUploader.__pathify(FileUploader.__file_upload_base_dir)
        del_dir(base_path+'/'+token)
    
    @staticmethod
    def remove_tokens(tokens):
        for token in tokens:
            FileUploader.remove_upload(token)
    
    @staticmethod
    def retrieve_contents_from_token(token):
        base_path = FileUploader.__pathify(FileUploader.__file_upload_base_dir)
        dir_path=base_path+'/'+token
        contents = read_contents_from_dir(dir_path)
        contents = reduce((lambda x,y: x+'\n'+y), contents)
        return contents
    
    @staticmethod
    def retrieve_contents_from_tokens(tokens):
        contents = []
        for token in tokens:
            contents.append(FileUploader.retrieve_contents_from_token(token))
        return contents