import logging
from logging.config import dictConfig
from logging_playground.utils import BaseLoggingTest


class TestDisableExistingLoggers(BaseLoggingTest):

    def test_disable_existing_loggers(self):
        """
        When `disable_existing_loggers` is False, any loggers from the initial
        config which aren't redefined are kept.
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
                'another_module': {
                    'handlers': ['test'],
                }
            }
        })
        log_msg = "This is a test"

        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'test2': {
                    'class': 'logging_playground.utils.MockLoggingHandler2',
                },
            },
            'loggers': {
                'my_module.child': {
                    'handlers': ['test2'],
                },
            }
        })
        logging.getLogger('my_module.child').error(log_msg)
        self.assertEqual(len(self.get_mock_logs(logging.ERROR)), 1)
        self.assertEqual(len(self.get_mock_logs2(logging.ERROR)), 1)
        logging.getLogger('another_module').error(log_msg)
        self.assertEqual(len(self.get_mock_logs(logging.ERROR)), 2)

    def test_disable_existing_loggers_true(self):
        """
        When `disable_existing_loggers` is True, any loggers from the initial
        config are disabled. This is unintuitive in that it does not overwrite
        the entire logging config. It does not even disable all the "loggers".
        If a logger is defined in the second config and its parent is defined
        in the first config. The first config is kept. Only loggers which do
        not have children defined in the second config will be disabled.
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
                'another_module': {
                    'handlers': ['test'],
                }
            }
        })
        log_msg = "This is a test"

        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'handlers': {
                'test2': {
                    'class': 'logging_playground.utils.MockLoggingHandler2',
                },
            },
            'loggers': {
                'my_module.child': {
                    'handlers': ['test2'],
                },
            }
        })
        # Empty! This logger is disabled!
        logging.getLogger('another_module').error(log_msg)
        self.assertEqual(len(self.get_mock_logs(logging.ERROR)), 0)

        logging.getLogger('my_module.child').error(log_msg)
        # This logger is defined in the second config
        self.assertEqual(len(self.get_mock_logs2(logging.ERROR)), 1)
        # This logger is defined in the initial config. Because it has a child
        # defined in the second config, it remains enabled and the log record
        # propagates to it.
        self.assertEqual(len(self.get_mock_logs(logging.ERROR)), 1)