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

    def getindices(self, record):
        indices = getattr(record, "indices", [])
        indices.append(getattr(record, "index", None))

        return indices

    def emit(self, record):
        for index in self.getindices(record):
            value = record.msg
            if isinstance(value, type({})):
                self.emitdictlike(value, index)
            else:
                self.emitsimple(value, index)

    def emitvalue(self, value, index):
        raise NotImplementedError()

    def emitdict(self, value, index):
        raise NotImplementedError()

    def emittuple(self, value, index):
        raise NotImplementedError()

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
    def emitsimple(self, value, index):
        self.indices[index] = self.indices.setdefault(index, 0) + value

    def emitdictlike(self, value, index):
        sub = self.indices.setdefault(index, {})
        for k, v in value.items():
            sub[k] = sub.setdefault(k, 0) + v

class Top(StatzHandler):
    pass
