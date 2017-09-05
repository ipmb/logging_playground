import logging
from logging_playground.utils import BaseLoggingTest


class TestInheritance(BaseLoggingTest):
    """
    Test how parent/children inherit configurations and the effect of
    redefining the same logger.
    """

    def test_child_inheritance(self):
        """
        Defined children should also use the parent config
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
                'my_module': {
                  'handlers': ['test'],
                },
                'my_module.child': {
                    'handlers': ['test2']
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module.child').error(log_msg)
        # Logs to its own handler
        self.assertMockLog2(logging.ERROR, [log_msg])
        # ...as well as the parent handler
        self.assertMockLog(logging.ERROR, [log_msg])

    def test_child_inheritance_identical(self):
        """
        Defined children follow the parent config, even if it is identical
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
            },
            'loggers': {
                'my_module': {
                  'handlers': ['test'],
                },
                'my_module.child': {
                    'handlers': ['test']
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module.child').error(log_msg)
        # logs to its own handler and the parent handler
        # since they are the same handler, the message is duplicated
        self.assertMockLog(logging.ERROR, [log_msg, log_msg])

    def test_redefinition(self):
        """
        Redefining the logger, replaces the initial definition
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test'],
                },
            }
        })

        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test2': {
                    'class': 'logging_playground.utils.MockLoggingHandler2',
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test2'],
                },
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # Initially defined handler is empty
        self.assertMockLog(logging.ERROR, [])
        # Last defined handler is used
        self.assertMockLog2(logging.ERROR, [log_msg])