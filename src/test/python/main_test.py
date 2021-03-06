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


import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('__file__')), '../../../src/main/python/'))

import unittest   # second test
from lib.utils import debug
from backend.database import SQLDatabase
from backend.category import Category
from lib.config import Config
from testcase.category_test import CategoryTest
from testcase.file_datastore_test import FileDataStoreTest
from testcase.file_upload_test import FileUploadTest
from testcase.query_processor_test import QueryProcessorTest
from testcase.request_ticket_system_test import RequestTicketSystemTest
from testcase.sqldatabase_test import SQLDatabaseTest
from testcase.query_accuracy_test import QueryAccuracyTest
from testcase.cache_layer_test import CacheLayerTest

#Here the ai stuffs
from testcase.ai_builder_reader_test import AIBuilderReaderTest
from testcase.sentence_corrector_test import SentenceCorrectorTest


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    _test_file='test-sqldb.db'
    SQLDatabase._db_location = _test_file
    
    _category = None
    _test_dir=join(abspath(dirname('__file__')), '../../../config/test/')
    config_file = _test_dir + 'setup-test.yaml'
    Config.Instance().set_config_path(config_file)
    Config.Instance().set_mode('prod')
    
    Config.Instance().set_version_file_path(join(abspath(dirname('__file__')), '../../../doc/version.txt'))
        
    _category=Category.Instance()
    cat_file = _test_dir +'test-category-production.txt'
    _category.set_path(cat_file)
    
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CategoryTest))
    test_suite.addTest(unittest.makeSuite(FileDataStoreTest))
    test_suite.addTest(unittest.makeSuite(FileUploadTest))
    test_suite.addTest(unittest.makeSuite(QueryProcessorTest))
    test_suite.addTest(unittest.makeSuite(RequestTicketSystemTest))
    test_suite.addTest(unittest.makeSuite(SQLDatabaseTest))
    test_suite.addTest(unittest.makeSuite(QueryAccuracyTest))
    test_suite.addTest(unittest.makeSuite(CacheLayerTest))
    test_suite.addTest(unittest.makeSuite(AIBuilderReaderTest))
    test_suite.addTest(unittest.makeSuite(SentenceCorrectorTest))
    
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)