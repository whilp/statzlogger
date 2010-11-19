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
    
    def record(self, *args, **kwargs):
        return FakeRecord(*args, **kwargs)
    
    def test_getindices(self):
        obj = self.init()
        record = self.record("foo", extra=dict(
            index="index",
        ))
        indices = obj.getindices(record)
        self.assertEqual(indices, ["index"])

class CollectionTests(unittest.TestCase):

    def cls(self):
        from statzlogger import Collection as cls
        return cls
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)

if __name__ == "__main__":
    unittest.main()
