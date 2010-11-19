import logging

try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger("statzlogger")
log.addHandler(NullHandler())

class Collection(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.indexes = {}

    def emit(self, record):
        log.debug("Got record: %s", record)

class Sum(logging.Handler):
    pass

class Top(logging.Handler):
    pass
