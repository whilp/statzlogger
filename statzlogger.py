import logging
import operator
import types

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
        logging.Handler.__init__(self, level=level)
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

    def __init__(self, level=logging.NOTSET, default=0, op=operator.add):
        StatzHandler.__init__(self, level=level)
        self.default = default
        self.op = op

    def emitvalue(self, value, index):
        value = self.op(self.indices.setdefault(index, self.default), value)
        StatzHandler.emitvalue(self, value, index)

class Collection(Sum):

    def __init__(self, level=logging.NOTSET, default=[], op=operator.add):
        Sum.__init__(self, level=level, default=default, op=op)

    def getvalue(self, record):
        return [Sum.getvalue(self, record)]

class Maximum(Collection):

    def __init__(self, level=logging.NOTSET, size=None, weight=1, reverse=True):
        Collection.__init__(self, level=level, default=[])
        self.size = size
        self.weight = weight
        self.reverse = reverse

    def getvalue(self, record):
        (value,) = Collection.getvalue(self, record)
        weight = getattr(record, "weight", self.weight)
        if callable(weight):
            weight = weight(value)
        return [(value, weight)]

    def emitvalue(self, value, index):
        Collection.emitvalue(self, value, index)
        self.indices[index] = sorted(self.indices[index],
                key=operator.itemgetter(1), 
                reverse=self.reverse)[:self.size]

class Minimum(Maximum):

    def __init__(self, level=logging.NOTSET, size=None, weight=1, reverse=False):
        Maximum.__init__(self, level=level, size=size, weight=weight, reverse=reverse)

class Set(Collection):

    def __init__(self, level=logging.NOTSET, default=set(), size=None, op=set.union):
        Collection.__init__(self, level=level, default=default, op=op)
        self.size = size

    def getvalue(self, record):
        value = Sum.getvalue(self, record)
        if isinstance(value, types.StringTypes):
            value = [value]
        return set(value)
    
    def emitvalue(self, value, index):
        Collection.emitvalue(self, value, index)
        if self.size is not None and len(self.indices[index]) > self.size:
            del(self.indices[index])

class Top(StatzHandler):
    pass
