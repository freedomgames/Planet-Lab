"""Test the common.resource module."""


import unittest

import backend.common.resource as resource


class TestRequestParser(unittest.TestCase):
    """Test the RequestParser class."""

    def test_add_argument(self):
        """Test our over-ride of the add_argument method."""
        parser = resource.RequestParser()
        parser.add_argument('snakes')
        parser.add_argument('ladders', required=True, type=int)
        parser.add_argument('cats', required=False, type=int)

        # no type is given, default behaviour
        self.assertEqual(parser.args[0].type('abc'), 'abc')

        # required, raise errors for None
        self.assertRaises(ValueError, parser.args[1].type, None)
        self.assertEqual(parser.args[1].type('1'), 1)

        # not required, return None without failing to call int() on it
        self.assertEqual(parser.args[2].type(None), None)
        self.assertEqual(parser.args[2].type('1'), 1)


if __name__ == '__main__':
    unittest.main()
