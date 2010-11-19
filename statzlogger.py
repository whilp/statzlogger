__license__ = """\
Copyright (c) 2010 Will Maier <willmaier@ml1.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import logging
import operator

__all__ = ["StatzHandler", "Sum", "Collection", "Maximum", "Minimum", "Set"]

try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger("statzlogger")
log.addHandler(NullHandler())

class StatzHandler(logging.Handler):
    """A basic handler to receive statistics in the form of LogRecords.

    The StatzHandler knows how to index and aggregate LogRecords. Various
    subclasses may aggregate records differently, but they all maintain a
    *indices* attribute. *indices* is a dictionary with keys accumulated during
    a logging run; its values are the logged data aggregated by index.

    These handlers rely on extra information supplied when a LogRecord is
    created (see :meth:`getvalue`). Instantiation of a StatzHandler is no
    different from that of a normal Handler.
    """
    indices = {}
    """A dictionary of indices.

    :meth:`emit` stores new record values after determining the appropriate
    index for a record (see :meth:`getindices`).
    """

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
        """Return the value of a LogRecord instance.

        If *record* has a *value* attribute, use that. Otherwise, use its *msg*
        attribute. Note: LogRecords can be given (nearly) arbitrary attributes
        at creation time by passing the *extra* keyword argument to the logging
        method. For example::

            >>> logging.debug("a message", extra={"value": "the real value"})
        """
        return getattr(record, "value", record.msg)

    def emit(self, record):
        """Emit the record.

        Typically, this means aggregating it in one of the handler's indices
        (under :attr:`indices`).
        """
        for index in self.getindices(record):
            value = self.getvalue(record)
            self.emitvalue(value, index)

    def emitvalue(self, value, index):
        """Emit a value for a single index."""
        self.indices[index] = value

class Sum(StatzHandler):
    """The arithmetic sum of the value of each record.

    Doesn't make sense for eg string values, but the implementation won't
    complain. Parameters:

        * *default* starting value
        * *op* operator to add values together
    """

    def __init__(self, level=logging.NOTSET, default=0, op=operator.add):
        StatzHandler.__init__(self, level=level)
        self.default = default
        self.op = op

    def emitvalue(self, value, index):
        value = self.op(self.indices.setdefault(index, self.default), value)
        StatzHandler.emitvalue(self, value, index)

class Collection(Sum):
    """A collection of records values."""

    def __init__(self, level=logging.NOTSET, default=[], op=operator.add):
        Sum.__init__(self, level=level, default=default, op=op)

    def getvalue(self, record):
        return [Sum.getvalue(self, record)]

class Maximum(Collection):
    """Keep only the values with the highest weight.

    In addition to the usual *msg* or *value* attributes, a LogRecord may set a
    *weight* attribute to influence the record's place in the sorted collection.
    Parameters:

        * *size* maximum size of each index
        * *weight* default record weight
        * *reverse* direction in which to sort the collection
    """

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
    """Keep only the values with the lowest weight."""

    def __init__(self, level=logging.NOTSET, size=None, weight=1, reverse=False):
        Maximum.__init__(self, level=level, size=size, weight=weight, reverse=reverse)

class Set(Collection):
    """A collection of unique items.

    If any index grows beyond *size* members, the entire index is removed.
    """

    def __init__(self, level=logging.NOTSET, default=set(), size=None, op=set.union):
        Collection.__init__(self, level=level, default=default, op=op)
        self.size = size

    def getvalue(self, record):
        value = Collection.getvalue(self, record)
        try:
            return set(value)
        except TypeError:
            return set(*value)
    
    def emitvalue(self, value, index):
        Collection.emitvalue(self, value, index)
        if self.size is not None and len(self.indices[index]) > self.size:
            del(self.indices[index])

class Top(StatzHandler):
    pass
