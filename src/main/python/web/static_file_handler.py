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

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import tornado.httpserver
import tornado.ioloop
import tornado.web
import posixpath
import os
import mimetypes
import pkg_resources
from lib.utils import debug

class StaticFileHandler(tornado.web.RequestHandler):
    
    def get_internal(self, pre_path, path):
        # Path checking taken from Flask's safe_join function:
        # https://github.com/mitsuhiko/flask/blob/1d55b8983/flask/helpers.py#L563-L587
        #debug()
        path = posixpath.normpath(path)
        if os.path.isabs(path) or path.startswith(".."):
            return self.send_error(404)

        extension = os.path.splitext(path)[1]
        if extension in mimetypes.types_map:
            self.set_header("Content-Type", mimetypes.types_map[extension])
        data = pkg_resources.resource_string(__name__, os.path.join(pre_path, path))
        #log.info(data)
        self.write(data)