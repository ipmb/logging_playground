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