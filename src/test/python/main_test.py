#import usertest
#import configtest # first test
import unittest   # second test
from category_test import CategoryTest
from file_datastore_test import FileDataStoreTest
from file_upload_test import FileUploadTest
from query_processor_test import QueryProcessorTest
from request_ticket_system_test import RequestTicketSystemTest
from sqldatabase_test import SQLDatabaseTest


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CategoryTest))
    test_suite.addTest(unittest.makeSuite(FileDataStoreTest))
    test_suite.addTest(unittest.makeSuite(FileUploadTest))
    test_suite.addTest(unittest.makeSuite(QueryProcessorTest))
    test_suite.addTest(unittest.makeSuite(RequestTicketSystemTest))
    test_suite.addTest(unittest.makeSuite(SQLDatabaseTest))
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)