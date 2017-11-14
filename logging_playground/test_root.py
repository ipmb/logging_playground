import logging
from textwrap import dedent

from logging_playground.utils import BaseLoggingTest


class TestRoot(BaseLoggingTest):
    """
    What does the "root" logger do?
    """

    def test_root_keyword(self):
        """
        You can use the ``root`` keyword to configure the root logger
        """
        logging.config.dictConfig({
            'version': 1,
            'root': {
                'level': 'ERROR',
            },
        })

        self.assertLogTree(dedent("""
            <--""
               Level ERROR"""))

    def test_root_as_empty_logger(self):
        """
        You can also use an empty logger name
        """
        logging.config.dictConfig({
            'version': 1,
            'loggers': {
                '': {
                    'level': 'ERROR',
                }
            },
        })

        self.assertLogTree(dedent("""
            <--""
               Level ERROR"""))

    def test_root_applies_globally(self):
        """
        All modules use the root logger
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['test'],
                },
            }
        })

        log_msg = "This is a test"

        # root applies to modules that aren't defined
        logging.getLogger('not_defined_module').error(log_msg)
        self.assertMockLog(logging.ERROR, [log_msg])

    def test_root_inheritance(self):
        """
        Inheritance works the same with the root logger
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
                'test2': {
                    'class': 'logging_playground.utils.MockLoggingHandler2',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['test'],
                },
                'my_module': {
                    'handlers': ['test2']
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # logs to its own logger
        self.assertMockLog2(logging.ERROR, [log_msg])
        # ...as well as the root logger
        self.assertMockLog(logging.ERROR, [log_msg])

    def test_root_inheritance(self):
        """
        Inheritance works the same with the root logger
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
                'test2': {
                    'class': 'logging_playground.utils.MockLoggingHandler2',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['test'],
                },
                'my_module': {
                    'handlers': ['test2']
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # logs to its own logger
        self.assertMockLog2(logging.ERROR, [log_msg])
        # ...as well as the root logger
        self.assertMockLog(logging.ERROR, [log_msg])

    def test_no_root_inheritance(self):
        """
        Don't propagate to root logger
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
                'null': {
                    'class': 'logging.NullHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['test'],
                },
                'my_module': {
                    'propagate': False,
                    'handlers': ['null'],
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # does not log anywhere
        self.assertMockLog(logging.ERROR, [])
        # children don't either
        logging.getLogger('my_module.child').error(log_msg)
        self.assertMockLog(logging.ERROR, [])