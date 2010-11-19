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
        """Return a list of indices for a given record.

        The list of indices will either contain the record's *index*
        attribute or a list generated from its iterable *indices*
        attribute. If both attributes are present, *index* will be
        added to *indices*.
        """
        index = getattr(record, "index", None)
        indices = list(getattr(record, "indices", []))
        if index is not None:
            indices.append(index)

        return indices

    def emit(self, record):
        for index in self.getindices(record):
            value = record.msg
            self.emitvalue(value, index)

    def emitvalue(self, record, index):
        raise NotImplementedError()

class Collection(StatzHandler):

    def emitvalue(self, value, index):
        self.indices.setdefault(index, []).append(value)

class Sum(StatzHandler):

    def __init__(self, level=logging.NOTSET, start=0):
        StatzHandler.__init__(self, level)
        self.start = start

    def emitvalue(self, value, index):
        self.indices[index] = self.indices.setdefault(index, 0) + value

class Top(StatzHandler):
    pass
