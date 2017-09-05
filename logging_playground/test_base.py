from importlib import reload
import logging
from logging.config import dictConfig

from logging_playground.utils import BaseLoggingTest

DEFAULT_TREE = """
<--""
   Level WARNING"""


class TestBaseLoggingTest(BaseLoggingTest):
    """
    Verify base test case resets logging correctly
    """

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