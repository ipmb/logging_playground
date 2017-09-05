import logging
from logging_playground.utils import BaseLoggingTest


class TestPropagate(BaseLoggingTest):

    def test_propagate_true(self):
        """
        When propagate is True, child modules will step up the tree
        to use parent handlers.
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
                    'propagate': True,  # this is the default
                }
            }
        })

        log_msg = "This is a test"

        logging.getLogger('my_module.child').error(log_msg)
        self.assertMockLog(logging.ERROR, [log_msg])
        # This applies to children that are not defined in the config as well
        logging.getLogger('my_module.child.grandchild').error(log_msg)
        self.assertMockLog(logging.ERROR, [log_msg, log_msg])

    def test_propagate_false(self):
        """
        When propagate is False, child modules will NOT step up the tree
        to use parent handlers.
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
                    'propagate': False,
                }
            }
        })
        log_msg = "This is a test"
        logging.getLogger('my_module.child').error(log_msg)
        self.assertMockLog(logging.ERROR, [])
        # This applies to children that are not defined in the config as well
        logging.getLogger('my_module.child.grandchild').error(log_msg)
        self.assertMockLog(logging.ERROR, [])

