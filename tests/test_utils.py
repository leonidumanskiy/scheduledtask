import unittest
from datetime import datetime
from scheduledtask import utils


class TestUtils(unittest.TestCase):
    def test_get_biggest_value_less_or_equal_to(self):
        self.assertEqual(utils.get_biggest_value_less_or_equal_to([1, 2, 3], 2), 2)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to([1, 5, 10], 7), 5)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to([1, 5, 15], 16), 15)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to([5, 15, 30], 3), None)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(5, 15), 10), 10)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(5, 15), 20), 14)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(5, 15), 3), None)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(5, 10, 2), 7), 7)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(5, 10, 2), 8), 7)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(7, 30, 5), 7), 7)
        self.assertEqual(utils.get_biggest_value_less_or_equal_to(range(7, 30, 5), 15), 12)

    def test_get_smallest_value_greater_or_equal_to(self):
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to([1, 2, 3], 2), 2)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to([1, 5, 10], 7), 10)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to([1, 5, 15], 16), None)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to([5, 15, 30], 3), 5)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(5, 15), 10), 10)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(5, 15), 20), None)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(5, 15), 3), 5)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(5, 10, 2), 7), 7)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(5, 10, 2), 8), 9)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(7, 30, 5), 7), 7)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(7, 30, 5), 15), 17)
        self.assertEqual(utils.get_smallest_value_greater_or_equal_to(range(7, 30, 5), 26), 27)

    def test_first(self):
        self.assertEqual(utils.first([1, 2, 3]), 1)
        self.assertEqual(utils.first(range(2, 15)), 2)

    def test_last(self):
        self.assertEqual(utils.last([1, 2, 3]), 3)
        self.assertEqual(utils.last(range(2, 15)), 14)
        self.assertEqual(utils.last(range(5, 10, 2)), 9)
        self.assertEqual(utils.last(range(7, 30, 5)), 27)

    def test_num_days_in_month(self):
        self.assertEqual(utils.num_days_in_month(2016, 12), 31)
        self.assertEqual(utils.num_days_in_month(2016, 2), 29)
        self.assertEqual(utils.num_days_in_month(2015, 2), 28)

    def test_weekday_num(self):
        self.assertEqual(utils.weekday_num(datetime(2016, 11, 17)), 2)
        self.assertEqual(utils.weekday_num(datetime(2016, 12, 31)), 4)
        self.assertEqual(utils.weekday_num(datetime(2017, 1, 31)), 4)

    def test_weekday_and_num_to_day(self):
        self.assertEqual(utils.weekday_and_num_to_day(2016, 11, 2, 3), 17)
        self.assertEqual(utils.weekday_and_num_to_day(2016, 12, 4, 5), 31)
        self.assertEqual(utils.weekday_and_num_to_day(2017, 1, 4, 1), 31)

    def test_weekday_and_week_to_day(self):
        self.assertEqual(utils.weekday_and_week_to_day(2016, 11, 0, 0), None)  # No Monday during first week of November
        self.assertEqual(utils.weekday_and_week_to_day(2016, 11, 4, 2), 30)
        self.assertEqual(utils.weekday_and_week_to_day(2016, 11, 2, 4), 18)
        self.assertEqual(utils.weekday_and_week_to_day(2017, 4, 0, 5), 1)
        self.assertEqual(utils.weekday_and_week_to_day(2016, 11, 4, 3), None)  # No Thursday during 5th week of November

    def test_week_num(self):
        self.assertEqual(utils.week_num(datetime(2016, 11, 1)), 0)
        self.assertEqual(utils.week_num(datetime(2016, 11, 5)), 0)
        self.assertEqual(utils.week_num(datetime(2016, 11, 6)), 0)
        self.assertEqual(utils.week_num(datetime(2016, 11, 7)), 1)
        self.assertEqual(utils.week_num(datetime(2016, 11, 30)), 4)
        self.assertEqual(utils.week_num(datetime(2016, 11, 30)), 4)
        self.assertEqual(utils.week_num(datetime(2017, 1, 31)), 5)
        self.assertEqual(utils.week_num(datetime(2017, 4, 1)), 0)
        self.assertEqual(utils.week_num(datetime(2017, 4, 23)), 3)
        self.assertEqual(utils.week_num(datetime(2017, 4, 30)), 4)

    def test_max_week_num(self):
        self.assertEqual(utils.max_week_num(2016, 11), 4)
        self.assertEqual(utils.max_week_num(2016, 12), 4)
        self.assertEqual(utils.max_week_num(2017, 1), 5)
        self.assertEqual(utils.max_week_num(2017, 4), 4)
