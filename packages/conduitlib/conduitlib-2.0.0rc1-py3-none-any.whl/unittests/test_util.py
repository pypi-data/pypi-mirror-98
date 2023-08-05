import unittest
from conduitlib import util

if __name__ == '__main__':
    unittest.main()


class TestGetClassLogger(unittest.TestCase):
    def test(self):
        expected = 'unittests.test_util.TestGetClassLogger'
        actual = util.get_class_logger(self).name
        self.assertEqual(expected, actual)
