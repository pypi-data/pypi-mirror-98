import unittest

from .time import current_millis, millis_to_datetime, datetime_to_millis


class TimeTest(unittest.TestCase):
    def test_current_millis(self):
        self.assertGreater(current_millis(), 0)
