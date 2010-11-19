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

    def getvalue(self, record):
        return record.msg

    def emit(self, record):
        for index in self.getindices(record):
            value = self.getvalue(record)
            self.emitvalue(value, index)

    def emitvalue(self, value, index):
        self.indices[index] = value

class Sum(StatzHandler):

    def __init__(self, level=logging.NOTSET, default=0):
        StatzHandler.__init__(self, level)
        self.default = default

    def emitvalue(self, value, index):
        value = self.indices.setdefault(index, self.default) + value
        StatzHandler.emitvalue(self, value, index)

class Collection(Sum):

    def __init__(self, level=logging.NOTSET, default=[]):
        Sum.__init__(self, level, default=default)

    def getvalue(self, record):
        return [Sum.getvalue(self, record)]

class Maximum(Collection):

    def __init__(self, level=logging.NOTSET, size=None, weight=1):
        Collection.__init__(self, level, default=[])
        self.size = size
        self.weight = weight

    def getvalue(self, record):
        weight = getattr(record, "weight", self.weight)
        if callable(weight):
            weight = weight(record)
        return (record.msg, weight)

    def emitvalue(self, value, index):
        StatzHandler.emitvalue(self, value, index)
        self.indices[index] = 
        self.indices[index] = sorted(self.indices[index], key=0)

class Top(StatzHandler):
    pass
