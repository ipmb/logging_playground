import logging
from logging_playground.utils import BaseLoggingTest


class TestLogLevels(BaseLoggingTest):
    """
    How do log levels defined at the handler or logging level play together?
    """

    def test_logger_above_handler(self):
        """
        Logger has a more restrictive level than the handler
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                    'level': 'INFO'
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test'],
                    'level': 'WARNING',
                },
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # Passes both handler and logger level
        self.assertMockLog(logging.ERROR, [log_msg])
        # Passes handler, but not logger: not logged
        logging.getLogger('my_module').info(log_msg)
        self.assertMockLog(logging.INFO, [])

    def test_logger_below_handler(self):
        """
        Logger has a less restrictive level than the handler
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                    'level': 'WARNING'
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test'],
                    'level': 'INFO',
                },
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').error(log_msg)
        # Passes both handler and logger level
        self.assertMockLog(logging.ERROR, [log_msg])
        # Passes logger, but not handler`: not logged
        logging.getLogger('my_module').info(log_msg)
        self.assertMockLog(logging.INFO, [])

    def test_logger_child_level(self):
        """
        Loggers propagate even when using the same handler, but only when both
        levels are satisfied.
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                    'level': 'INFO'
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test'],
                    'level': 'INFO',
                },
                'my_module.child': {
                    'handlers': ['test'],
                    'level': 'WARNING',
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module.child').info(log_msg)
        # Does not log to logger for `my_module`
        self.assertMockLog(logging.INFO, [])
        # Logs to both `my_module` and `my_module.child`
        logging.getLogger('my_module.child').warning(log_msg)
        self.assertMockLog(logging.WARNING, [log_msg, log_msg])

    def test_notset_level(self):
        """
        Logging can be disabled altogether by using the `NOTSET` level
        """
        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'test': {
                    'class': 'logging_playground.utils.MockLoggingHandler',
                    'level': 'DEBUG'
                },
            },
            'loggers': {
                'my_module': {
                    'handlers': ['test'],
                    'level': 'NOTSET',
                },
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module').info(log_msg)
        # Does not log on debug level
        self.assertMockLog(logging.INFO, [])
        # Doesn't even log if we use NOTSET as the level
        logging.getLogger('my_module').log(logging.NOTSET, log_msg)
        self.assertMockLog(logging.NOTSET, [])