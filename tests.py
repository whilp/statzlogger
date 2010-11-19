import unittest

class StatzHandlerTests(unittest.TestCase):

    def cls(self):
        from statzlogger import StatzHandler
        return StatzHandler
    
    def init(self, *args, **kwargs):
        return self.cls()(*args, **kwargs)
