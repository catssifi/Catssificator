#!/usr/bin/python
# Copyright (c) 2015 Ken Wu
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

import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))

import unittest   # second test
from lib.utils import debug
from testcase.sentence_corrector_test import SentenceCorrectorTest
from testcase.ai_database_builder_test import AIDatabaseBuilderTest
from backend.database import SQLDatabase
from lib.config import Config

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    _test_file='test-sqldb.db'
    SQLDatabase._db_location = _test_file
    
    _test_dir=join(abspath(dirname('__file__')), '../../../config/test/')
    config_file = _test_dir + 'setup-test.yaml'
    Config.Instance().set_config_path(config_file)
    Config.Instance().set_mode('prod')  
    
    Config.Instance().set_version_file_path(join(abspath(dirname('__file__')), '../../../doc/version.txt'))    
    
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(AIDatabaseBuilderTest))
    #test_suite.addTest(unittest.makeSuite(SentenceCorrectorTest))
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)