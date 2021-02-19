import unittest

from pyhello import HelloPython


class TestHelloCase(unittest.TestCase):
    def test_hello(self):
        hs = HelloPython()
        self.assertEqual(hs.say_hello(), 'Hello, Python!')


if __name__ == '__main__':
    unittest.main()
