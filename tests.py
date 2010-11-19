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

    def test_getvalue_value(self):
        obj = self.init()
        record = FakeRecord("wrongvalue",
                extra=dict(value="rightvalue"))
        value = obj.getvalue(record)
        self.assertEqual(value, "rightvalue")

    def test_getvalue_str(self):
        obj = self.init()
        record = FakeRecord("value")
        value = obj.getvalue(record)
        self.assertEqual(value, "value")

    def test_getvalue_int(self):
        obj = self.init()
        record = FakeRecord(1)
        value = obj.getvalue(record)
        self.assertEqual(value, 1)

    def test_getvalue_seq(self):
        obj = self.init()
        record = FakeRecord((1,2,3))
        value = obj.getvalue(record)
        self.assertEqual(value, (1,2,3))

    def test_emitvalue(self):
        obj = self.init()
        obj.emitvalue("value", "index")
        self.assertEqual(obj.indices["index"], "value")

        obj.emitvalue("otherval", "index")
        self.assertEqual(obj.indices["index"], "otherval")

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

        obj.emitvalue(2, "index")
        self.assertEqual(obj.indices, {"index": 3})

    def test_emitvalue_with_default(self):
        obj = self.init(default=10)
        obj.emitvalue(1, "index")
        self.assertEqual(obj.indices, {"index": 11})

        obj.emitvalue(1, "index")
        self.assertEqual(obj.indices, {"index": 12})

class CollectionTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Collection as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

    def test_getvalue_str(self):
        obj = self.init()
        record = FakeRecord("value")
        value = obj.getvalue(record)
        self.assertEqual(value, ["value"])

    def test_getvalue_int(self):
        obj = self.init()
        record = FakeRecord(1)
        value = obj.getvalue(record)
        self.assertEqual(value, [1])

    def test_getvalue_seq(self):
        obj = self.init()
        record = FakeRecord((1,2,3))
        value = obj.getvalue(record)
        self.assertEqual(value, [(1,2,3)])

    def test_emitvalue(self):
        obj = self.init()
        obj.emitvalue([1], "index")
        self.assertEqual(obj.indices, {"index": [1]})

        obj.emitvalue([1], "index")
        self.assertEqual(obj.indices, {"index": [1, 1]})

class MaximumTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Maximum as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

    def test_getvalue_str(self):
        obj = self.init()
        record = FakeRecord("value")
        value = obj.getvalue(record)
        self.assertEqual(value, [("value", 1)])

    def test_getvalue_int(self):
        obj = self.init()
        record = FakeRecord(1)
        value = obj.getvalue(record)
        self.assertEqual(value, [(1, 1)])

    def test_getvalue_seq(self):
        obj = self.init()
        record = FakeRecord((1,2,3))
        value = obj.getvalue(record)
        self.assertEqual(value, [((1,2,3), 1)])

    def test_getvalue_weighted(self):
        obj = self.init()
        record = FakeRecord("value", extra=dict(weight=10))
        value = obj.getvalue(record)
        self.assertEqual(value, [("value", 10)])

    def test_emitvalue(self):
        obj = self.init()
        obj.emitvalue([("value", 1)], "index")
        self.assertEqual(obj.indices["index"], [("value", 1)])

        obj.emitvalue([("value", 2)], "index")
        self.assertEqual(len(obj.indices), 1)
        self.assertEqual(obj.indices["index"][0], ("value", 2))

    def test_emitvalue_size(self):
        obj = self.init(size=3)
        for i in range(5):
            obj.emitvalue([("value%d" % i, i)], "index")

        self.assertEqual(len(obj.indices["index"]), 3)
        self.assertEqual(obj.indices["index"][0], ("value4", 4))
        self.assertEqual(obj.indices["index"][-1], ("value2", 2))

class MinimumTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Minimum as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

    def test_emitvalue(self):
        obj = self.init()

        obj.emitvalue([("value1", 1)], "index")
        self.assertEqual(obj.indices["index"], [("value1", 1)])

        obj.emitvalue([("value2", 2)], "index")
        self.assertEqual(len(obj.indices["index"]), 2)
        self.assertEqual(obj.indices["index"][0], ("value1", 1))

class SetTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Set as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)
    
    def test_getvalue_str(self):
        obj = self.init()
        record = FakeRecord("value")
        value = obj.getvalue(record)
        self.assertEqual(value, set(["value"]))
    
    def test_getvalue_int(self):
        obj = self.init()
        record = FakeRecord(1)
        value = obj.getvalue(record)
        self.assertEqual(value, set([1]))

    def test_getvalue_seq(self):
        obj = self.init()
        record = FakeRecord(["one", "two"])
        value = obj.getvalue(record)
        self.assertEqual(value, set(("one", "two")))

    def test_emitvalue(self):
        obj = self.init()
        obj.emitvalue(["value"], "index")
        self.assertEqual(obj.indices["index"], set(["value"]))

        obj.emitvalue(["value"], "index")
        self.assertEqual(obj.indices["index"], set(["value"]))

    def test_emitvalue_size(self):
        obj = self.init(size=1)
        obj.emitvalue(["value"], "index")
        self.assertEqual(obj.indices["index"], set(["value"]))

        obj.emitvalue(["value"], "index")
        self.assertTrue(len(obj.indices), 0)


if __name__ == "__main__":
    unittest.main()
