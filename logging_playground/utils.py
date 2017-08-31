import logging
from collections import defaultdict

MESSAGES = defaultdict(list)
MESSAGES2 = defaultdict(list)


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