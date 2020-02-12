import unittest

from pystatmath import HelloStatmath


class HelloCase(unittest.TestCase):
    def test_hello(self):
        hs = HelloStatmath()
        self.assertEqual(hs.say_hello(), 'Hello, statmath!')


if __name__ == '__main__':
    unittest.main()
