import logging

try:
    NullHandler = logging.NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger().addHandler(NullHandler())

class StatsLogger(logging.Logger):
    """A statistics logger.

    Methods stolen from szl:
        collection: A simple collection or concatenation of the data.
        sample: A statistical sampling of N items.
        sum: An arithmetic sum of the data.
        top: Statistical samplings that record the `top N' data items.
        maximum: A precise sample of the N highest-weighted data items.
        minimum: A precise sample of the N lowest-weighted data items.
        unique: Statistical estimators for the total number of unique data items.
        set: A set of size at most N. Larger sets are discarded.
        quantile: Approximate quantiles (actually N-tiles) for data items from an ordered domain.
        distinctsample: A uniform sample of a given size from a set of all values seen.
        inversehistogram: An approximate histogram of unique values.
        weightedsample: A sample of a given size from a set of all values seen, biased towards values with higher weights.
        recordio: An unindexed collection written directly to a binary file.
        text: An unindexed collection written directly to a plain file.
        mrcounter: An integer counter that can be used to provide an accumulated count (e.g. a progress indicator) to a C++ program invoking the Sawzall interpreter.
    """

    def log(self, level, msg, *args, **kwargs):
        pass

class CollectionLogger(logging.Logger):

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        rv = LogRecord()
        return rv

class CollectionHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.collections = {}
    
    def emit(self, record):
        for index in record.indexes:
            self.collections.setdefault(index, []).append(record)

class SumHandler(logging.Handler):
    
    def __init__(self, level=logging.NOTSET):
        logging.Handler.__init__(self, level)
        self.

import logging

try:
    from statslogger import StatsLogger
except ImportError:
    class StatsLogger(logging.Logger):
        def stats(self, *args, **kwags):
            pass
logging.setLoggerClass(StatsLogger)

log = logging.getLogger("fans")
log.stats(("britney", "a britney song"), index=fan_age/10)

import statzlogger as szl



szl.collection("fans", ("britney", "a britney song"),
        index=fan_age/10)
szl.sum("divafans", 1, index="britney")
szl.sum("sales", 0.25, index=1)
szl.sum("sales.hourly", "
