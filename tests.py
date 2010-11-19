import unittest

class FakeRecord(object):

    def __init__(self, msg, extra={}):
        self.msg = msg
        for k, v in extra.items():
            setattr(self, k, v)

class StatzHandlerTests(unittest.TestCase):

    def cls(self):
        from statzlogger import StatzHandler as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

    def test_getindices_index(self):
        obj = self.init()
        record = FakeRecord("foo", extra=dict(
            index="index",
        ))
        indices = obj.getindices(record)
        self.assertEqual(indices, ["index"])

    def test_getindices_indices_tuple(self):
        obj = self.init()
        record = FakeRecord("foo", extra=dict(
            indices=("index1", "index2"),
        ))
        indices = obj.getindices(record)
        self.assertEqual(indices, ["index1", "index2"])

    def test_getindices_both(self):
        obj = self.init()
        record = FakeRecord("foo", extra=dict(
            index="index",
            indices=("index1", "index2"),
        ))
        indices = obj.getindices(record)
        self.assertEqual(indices, ["index1", "index2", "index"])

    def test_getindices_none(self):
        obj = self.init()
        record = FakeRecord("record")
        indices = obj.getindices(record)
        self.assertEqual(indices, [None])

    def test_emitvalue_noindex(self):
        obj = self.init()
        obj.emitvalue("value", "index")
        self.assertEqual(obj.indices["index"], "value")

class SumTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Sum as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

    def test_emitvalue(self):
        obj = self.init()
        obj.emitvalue(1, "index")
        self.assertEqual(obj.indices, {"index": 1})

class CollectionTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Collection as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

if __name__ == "__main__":
    unittest.main()
