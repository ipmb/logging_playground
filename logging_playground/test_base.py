from importlib import reload
import logging
from logging.config import dictConfig

import logging_tree
from logging_playground.utils import MockLoggingHandler, MockLoggingHandler2
import unittest

DEFAULT_TREE = """
<--""
   Level WARNING"""


def _get_tree():
    return logging_tree.format.build_description(None)[:-1]


class BaseLoggingTest(unittest.TestCase):
    """Resets logging config after each test"""
    def setUp(self):
        reload(logging)

    def tearDown(self):
        MockLoggingHandler().reset()
        MockLoggingHandler2().reset()
        logging.shutdown()

    def assertLogTree(self, expected):
        self.assertEqual(expected.strip(), _get_tree())

    def assertNotLogTree(self, expected):
        self.assertNotEqual(expected.strip(), _get_tree())

    def get_mock_logs(self, level):
        return MockLoggingHandler().messages[logging.getLevelName(level)]

    def get_mock_logs2(self, level):
        return MockLoggingHandler2().messages[logging.getLevelName(level)]

    def assertMockLog(self, level, expected):
        self.assertListEqual(self.get_mock_logs(level), expected)

    def assertMockLog2(self, level, expected):
        self.assertListEqual(self.get_mock_logs2(level), expected)



class TestBaseLoggingTest(BaseLoggingTest):

    def test_default_tree(self):
        self.assertLogTree(DEFAULT_TREE)

    def test_reset_tree(self):
        logging.config.dictConfig({
            'version': 1,
            'loggers': {
                'my_module': {}
            }
        })
        self.assertNotLogTree(DEFAULT_TREE)
        logging.shutdown()
        reload(logging)
        self.assertLogTree(DEFAULT_TREE)