"""Tests for the custom_types module."""


import datetime
import pytz
import unittest

import backend.common.custom_types as custom_types


class CustomTypesTest(unittest.TestCase):
    """Tests for the custom_types module."""

    def test_utc_date_time(self):
        """Test the UTCDateTime class."""
        utc_type = custom_types.UTCDateTime()
        # errors on naive datetimes
        self.assertRaises(
                ValueError,
                utc_type.process_bind_param,
                datetime.datetime(2012, 12, 21), None)

        # convert times to utc
        eastern = pytz.timezone('US/Eastern')
        local_time = eastern.normalize(datetime.datetime(
                2012, 12, 21, 12, tzinfo=eastern))
        utc_time = utc_type.process_bind_param(local_time, None)
        self.assertEqual(utc_time.tzinfo, pytz.utc)
        self.assertEqual(utc_time, datetime.datetime(
                2012, 12, 21, 16, 56, tzinfo=pytz.utc))

        # return non-naive datetimes in utc
        self.assertEqual(
                utc_type.process_result_value(
                    datetime.datetime(2012, 12, 21), None),
                datetime.datetime(2012, 12, 21, tzinfo=pytz.utc))
