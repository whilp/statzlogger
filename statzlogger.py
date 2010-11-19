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

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.indices = {}

    def emit(self, record):
        pass

class Collection(StatzHandler):

    def emit(self, record):
        indices = getattr(record, "indices", [])
        indices.append(getattr(record, "index", None))

        for index in indices:
            self.indices.setdefault(index, []).append(record)

class Sum(StatzHandler):

    def __init__(self, level=logging.NOTSET, start=0):
        StatzHandler.__init__(self, level)
        self.start = start

    def emit(self, record):
        indices = getattr(record, "indices", [])
        indices.append(getattr(record, "index", None))

        for index in indices:
            value = record.msg
            if isinstance(value, type({})):
                self.emitdictlike(value, index)
            else:
                self.emitsimple(value, index)

    def emitsimple(self, value, index):
        self.indices[index] = self.indices.setdefault(index, 0) + value

    def emitdictlike(self, value, index):
        sub = self.indices.setdefault(index, {})
        for k, v in value.items():
            sub[k] = sub.setdefault(k, 0) + v

class Top(StatzHandler):
    pass
