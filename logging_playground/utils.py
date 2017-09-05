from importlib import reload
import logging
import unittest
from collections import defaultdict

import logging_tree

MESSAGES = defaultdict(list)
MESSAGES2 = defaultdict(list)


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


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict,
    in order, indexed by a lowercase log level string (e.g., 'debug',
    'info', etc.).
    """
    messages = MESSAGES

    def emit(self, record):
        """
        Store a message from ``record``
        in the instance's ``messages`` dict.
        """
        self.messages[record.levelname].append(record.getMessage())

    def reset(self):
        for message_list in self.messages.values():
                message_list.clear()



class MockLoggingHandler2(MockLoggingHandler):
    messages = MESSAGES2