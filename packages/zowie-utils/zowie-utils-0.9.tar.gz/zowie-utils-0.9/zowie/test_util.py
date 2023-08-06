import unittest

from .util import head_option


class UtilTest(unittest.TestCase):
    def test_head_option(self):
        cases = [
            ([], None),
            ([1, 2, 3], 1),
        ]

        for seq, expected in cases:
            self.assertEqual(head_option(seq), expected)
