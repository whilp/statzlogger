import logging

try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger("statzlogger")
log.addHandler(NullHandler())

class StatzHandler(logging.Handler):

    def emit(self, record):
        pass

class Collection(StatzHandler):

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.indexes = {}

    def emit(self, record):
        log.debug("Got record: %s", record)

class Sum(StatzHandler):
    pass

class Top(StatzHandler):
    pass
