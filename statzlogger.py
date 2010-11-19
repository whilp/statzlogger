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

        The list of indices will either contain the record's *index* attribute
        or a list generated from its iterable *indices* attribute. If both
        attributes are present, *index* will be added to *indices*. If no
        indices are defined, the resulting list will be [None].
        """
        index = getattr(record, "index", None)
        indices = list(getattr(record, "indices", []))
        if index is not None:
            indices.append(index)
        if not indices:
            indices = [None]

        return indices

    def emit(self, record):
        for index in self.getindices(record):
            value = record.msg
            self.emitvalue(value, index)

    def emitvalue(self, value, index):
        self.indices[index] = value

class Sum(StatzHandler):

    def __init__(self, level=logging.NOTSET, default=0):
        StatzHandler.__init__(self, level)
        self.default = default

    def emitvalue(self, value, index):
        self.indices[index] = self.indices.setdefault(index, self.default) + value

class Collection(Sum):

    def __init__(self, level=logging.NOTSET, default=[]):
        Sum.__init__(self, level, default=default)

    def emitvalue(self, value, index):
        Sum.emitvalue(self, [value], index)

class Top(StatzHandler):
    pass
