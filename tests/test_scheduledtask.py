import unittest
from scheduledtask import ScheduledTask
from datetime import datetime


class TestScheduledTask(unittest.TestCase):
    def _test_previous(self, minutes=None, hours=None, days=None, days_of_week=None, days_of_week_num=None, weeks=None,
                       months=None, years=None, current_time=None, expected_result=None):
        """Common wrapper for get_previous_time test
        """
        task = ScheduledTask(minutes, hours, days, days_of_week, days_of_week_num, weeks, months, years)
        self.assertEqual(task.get_previous_time(current_time), expected_result)

    def _test_next(self, minutes=None, hours=None, days=None, days_of_week=None, days_of_week_num=None, weeks=None,
                   months=None, years=None, current_time=None, expected_result=None):
        """Common wrapper for get_next_time test
        """
        task = ScheduledTask(minutes, hours, days, days_of_week, days_of_week_num, weeks, months, years)
        self.assertEqual(task.get_next_time(current_time), expected_result)

    def test_previous_same_day(self):
        """0:45 same day
        """
        self._test_previous(minutes=[15, 45], hours=[0], days=None, months=None, years=None,
                            current_time=datetime(2016, 11, 12, 23, 0),
                            expected_result=datetime(2016, 11, 12, 0, 45))

    def test_previous_every_nth_day_of_month(self):
        """23:00 10th of November
        """
        self._test_previous(minutes=[0], hours=[23], days=[10], months=None, years=None,
                            # at 23:00 every 10th day of month
                            current_time=datetime(2016, 11, 12, 23, 0),  # 23:00 12/11/2016
                            expected_result=datetime(2016, 11, 10, 23, 0))  # 23:00 10/11/2016

    def test_previous_every_nth_day_of_month2(self):
        """15th last month
        """
        self._test_previous(minutes=[0], hours=[23], days=[15], months=None, years=None,
                            # at 23:00 every 15th day of month
                            current_time=datetime(2016, 11, 12, 23, 0),  # 23:00 12/11/2016
                            expected_result=datetime(2016, 10, 15, 23, 0))  # 23:00 15/10/2016

    def test_previous_31st_day_of_month(self):
        """31st of October, 2016
        """
        self._test_previous(minutes=[0], hours=[0], days=[31], months=None, years=None,
                            # at 00:00 31st day of month
                            current_time=datetime(2016, 12, 15, 0, 0),  # 00:00 15/12/2016
                            expected_result=datetime(2016, 10, 31, 0, 0))  # 00:00 31/10/2016

    def test_previous_every_nth_day_of_month_correct_minute(self):
        """15th last month, check for correct minute (30)
        """
        self._test_previous(minutes=[0, 30], hours=[0], days=[15], months=None, years=None,
                            # at 00:00 or 00:30 every 15th day of month
                            current_time=datetime(2016, 11, 12, 23, 0),  # 23:00 12/11/2016
                            expected_result=datetime(2016, 10, 15, 0, 30))     # 00:30 12/11/2016

    def test_previous_independence_day_this_year(self):
        """This year independence day, 4th of July
        """
        self._test_previous(minutes=[0], hours=[0], days=[4], months=[7], years=None,  # at 00:00 every 4th of July
                            current_time=datetime(2016, 11, 12, 0, 0),  # 00:00 12/11/2016
                            expected_result=datetime(2016, 7, 4, 0, 0))   # 00:00 04/07/2015

    def test_previous_independence_day_last_year(self):
        """Last year independence day, 4th of July
        """
        self._test_previous(minutes=[0], hours=[0], days=[4], months=[7], years=None,  # at 00:00 every 4th of July
                            current_time=datetime(2016, 3, 12, 0, 0),  # 00:00 12/11/2016
                            expected_result=datetime(2015, 7, 4, 0, 0))  # 00:00 04/07/2015

    def test_previous_every_30_minutes(self):
        """Last hour 00/30 minutes
        """
        self._test_previous(minutes=[0, 30], hours=None, days=None, months=None, years=None,
                            # every 30 mins, at 00 and 30th minute
                            current_time=datetime(2016, 11, 15, 19, 55),  # 19:55 15/11/2016
                            expected_result=datetime(2016, 11, 15, 19, 30))     # 19:30 15/11/2016

    def test_previous_31st_january(self):
        """January, 31st, when current month is March, 15th
        """
        self._test_previous(minutes=[0], hours=[0], days=[31], months=[1], years=None,  # January, 31st, at 00:00
                            current_time=datetime(2016, 3, 15, 0, 0),  # 00:00 15/3/2016
                            expected_result=datetime(2016, 1, 31, 0, 0))  # 00:00 31/1/2016

    def test_previous_31st_day_of_month_skip_feb(self):
        """31st day of month, when current month is March, 15th (should skip February since it doesn't have 31 days)
        """
        self._test_previous(minutes=[0], hours=[0], days=[31], months=None, years=None,
                            # Every 31st day of month, at 00:00
                            current_time=datetime(2016, 3, 15, 0, 0),  # 00:00 15/3/2016
                            expected_result=datetime(2016, 1, 31, 0, 0))  # 00:00 31/1/2016

    def test_previous_every_monday(self):
        """Every monday at 00:00, check this week
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[0], months=None, years=None,  # Every Monday at 00:00
                            current_time=datetime(2016, 11, 16, 15, 30),  # 15:30 16/11/2016 Wednesday
                            expected_result=datetime(2016, 11, 14, 0, 0))  # 00:00 14/11/2016 Monday

    def test_previous_every_friday(self):
        """Every friday at 00:00, check last week
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[4], months=None, years=None,  # Every Friday at 00:00
                            current_time=datetime(2016, 11, 16, 15, 30),  # 15:30 16/11/2016 Wednesday
                            expected_result=datetime(2016, 11, 11, 0, 0))  # 00:00 11/11/2016 Friday

    def test_previous_first_monday_of_november(self):  # Every first Monday of November
        """Every first Monday of November
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[0], days_of_week_num=[0], months=[11], years=None,
                            # Every first Monday of November
                            current_time=datetime(2016, 11, 17, 15, 30),  # 15:30 17/11/2016 Wednesday
                            expected_result=datetime(2016, 11, 7, 0, 0))  # 00:00 7/11/2016 Monday

    def test_previous_first_tuesday_of_november(self):  # Every first Tuesday of November
        """Every first Tuesday of November
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[1], days_of_week_num=[0], months=[11], years=None,
                            # Every first Tuesday of November
                            current_time=datetime(2016, 11, 16, 15, 30),  # 15:30 16/11/2016 Wednesday
                            expected_result=datetime(2016, 11, 1, 0, 0))  # 00:00 1/11/2016 Tuesday

    def test_previous_5th_saturday_of_december(self):  # Every last Saturday of December
        """Every 4th Saturday of December
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[5], days_of_week_num=[4], months=[12], years=None,
                            # Every 5th Saturday of December
                            current_time=datetime(2017, 1, 1, 00, 00),  # 00:00 01/01/2017 Sunday
                            expected_result=datetime(2016, 12, 31, 0, 0))  # 00:00 31/12/2016 Saturday

    def test_previous_5th_wednesday(self):  # Every 5th wednesday
        """Every 5th Wednesday
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[2], days_of_week_num=[4], months=None, years=None,
                            # Every 5th Wednesday
                            current_time=datetime(2017, 1, 31, 00, 00),  # 00:00 31/01/2017 Tuesday
                            expected_result=datetime(2016, 11, 30, 0, 0))  # 00:00 30/11/2016 Wednesday

    def test_previous_every_even_day(self):   # Every even day at 00:00
        """Every even day at 00:00
        """
        self._test_previous(minutes=[0], hours=[0], days=range(0, 31, 2), months=None, years=None,
                            # Every even day
                            current_time=datetime(2016, 11, 17, 15, 00),  # 15:00 17/11/2017 Thursday
                            expected_result=datetime(2016, 11, 16, 0, 0))  # 00:00 30/11/2016 Wednesday

    def test_previous_every_third_hour(self):   # Every third hour
        """Every third hour
        """
        self._test_previous(minutes=[0], hours=range(0, 24, 3), days=None, months=None, years=None,
                            # Every third hour
                            current_time=datetime(2016, 11, 17, 10, 00),  # 10:00 17/11/2017 Thursday
                            expected_result=datetime(2016, 11, 17, 9, 0))  # 9:00 17/11/2016 Thursday

    def test_previous_monday_before_presidential_election_day(self):  # Every first Monday of November every 4rth year
        """Every first Monday of November every 4rth year, starting from 1848
        """
        self._test_previous(minutes=[0], hours=[0], days_of_week=[0], days_of_week_num=[0], months=[11], years=range(1848, 9999, 4),
                            # Every first Monday of November, every 4rth year starting with 1848
                            current_time=datetime(2018, 11, 17, 15, 30),  # 15:30 17/11/2016 Wednesday
                            expected_result=datetime(2016, 11, 7, 0, 0))  # 00:00 7/11/2016 Monday

    def test_next_same_day(self):
        """0:45 same day
        """
        self._test_next(minutes=[15, 45], hours=[0], days=None, months=None, years=None,
                        current_time=datetime(2016, 11, 12, 0, 30),
                        expected_result=datetime(2016, 11, 12, 0, 45))

    def test_next_every_nth_day_of_month(self):
        """23:00 10th of November
        """
        self._test_next(minutes=[0], hours=[23], days=[10], months=None, years=None,
                        # at 23:00 every 10th day of month
                        current_time=datetime(2016, 11, 8, 23, 0),  # 23:00 8/11/2016
                        expected_result=datetime(2016, 11, 10, 23, 0))  # 23:00 10/11/2016

    def test_next_every_nth_day_of_month2(self):
        """15th next month
        """
        self._test_next(minutes=[0], hours=[23], days=[15], months=None, years=None,
                        # at 23:00 every 15th day of month
                        current_time=datetime(2016, 9, 20, 23, 0),  # 23:00 20/9/2016
                        expected_result=datetime(2016, 10, 15, 23, 0))  # 23:00 15/10/2016

    def test_next_31st_day_of_month(self):
        """31st of October, 2016
        """
        self._test_next(minutes=[0], hours=[0], days=[31], months=None, years=None,
                        # at 00:00 31st day of month
                        current_time=datetime(2016, 9, 15, 0, 0),  # 00:00 15/9/2016
                        expected_result=datetime(2016, 10, 31, 0, 0))  # 00:00 31/10/2016

    def test_next_every_nth_day_of_month_correct_minute(self):
        """15th next month, check for correct minute (30)
        """
        self._test_next(minutes=[0, 30], hours=[0], days=[15], months=None, years=None,
                        # at 00:00 or 00:30 every 15th day of month
                        current_time=datetime(2016, 9, 16, 23, 0),  # 23:00 16/9/2016
                        expected_result=datetime(2016, 10, 15, 0, 0))     # 00:30 12/11/2016

    def test_next_independence_day_this_year(self):
        """This year independence day, 4th of July
        """
        self._test_next(minutes=[0], hours=[0], days=[4], months=[7], years=None,  # at 00:00 every 4th of July
                        current_time=datetime(2016, 3, 12, 0, 0),  # 00:00 12/03/2016
                        expected_result=datetime(2016, 7, 4, 0, 0))   # 00:00 04/07/2016

    def test_next_independence_day_next_year(self):
        """Next year independence day, 4th of July
        """
        self._test_next(minutes=[0], hours=[0], days=[4], months=[7], years=None,  # at 00:00 every 4th of July
                        current_time=datetime(2014, 8, 15, 0, 0),  # 00:00 08/15/2014
                        expected_result=datetime(2015, 7, 4, 0, 0))  # 00:00 04/07/2015

    def test_next_every_30_minutes(self):
        """Next hour 00/30 minutes
        """
        self._test_next(minutes=[0, 30], hours=None, days=None, months=None, years=None,
                        # every 30 mins, at 00 and 30th minute
                        current_time=datetime(2016, 11, 15, 19, 5),  # 19:55 15/11/2016
                        expected_result=datetime(2016, 11, 15, 19, 30))     # 19:30 15/11/2016

    def test_next_1st_january(self):
        """January, 1st, when current month is March, 15th
        """
        self._test_next(minutes=[0], hours=[0], days=[1], months=[1], years=None,  # January, 1st, at 00:00
                        current_time=datetime(2016, 3, 15, 0, 0),  # 00:00 15/3/2016
                        expected_result=datetime(2017, 1, 1, 0, 0))  # 00:00 31/1/2016

    def test_next_31st_day_of_month_skip_feb(self):
        """31st day of month, when current month is January, 31st (should skip February since it doesn't have 31 days)
        """
        self._test_next(minutes=[0], hours=[0], days=[31], months=None, years=None,
                        # Every 31st day of month, at 00:00
                        current_time=datetime(2016, 1, 31, 15, 0),  # 15:00 31/1/2016
                        expected_result=datetime(2016, 3, 31, 0, 0))  # 00:00 31/3/2016

    def test_next_every_wednesday(self):
        """Every Wednesday at 00:00, check this week
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[2], months=None, years=None,  # Every Wednesday at 00:00
                        current_time=datetime(2016, 11, 15, 15, 30),  # 15:30 15/11/2016 Tuesday
                        expected_result=datetime(2016, 11, 16, 0, 0))  # 00:00 16/11/2016 Wednesday

    def test_next_every_monday(self):
        """Every monday at 00:00, check next week
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[0], months=None, years=None,  # Every Monday at 00:00
                        current_time=datetime(2016, 11, 16, 15, 30),  # 15:30 16/11/2016 Wednesday
                        expected_result=datetime(2016, 11, 21, 0, 0))  # 00:00 21/11/2016 Monday

    def test_next_first_monday_of_november(self):  # Every first Monday of November
        """Every first Monday of November
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[0], days_of_week_num=[0], months=[11], years=None,
                        # Every first Monday of November
                        current_time=datetime(2016, 10, 18, 15, 30),  # 15:30 18/10/2016 Tuesday
                        expected_result=datetime(2016, 11, 7, 0, 0))  # 00:00 7/11/2016 Monday

    def test_next_first_tuesday_of_november(self):  # Every first Tuesday of November
        """Every first Tuesday of November
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[1], days_of_week_num=[0], months=[11], years=None,
                        # Every first Tuesday of November
                        current_time=datetime(2016, 10, 16, 15, 30),  # 15:30 16/10/2016 Monday
                        expected_result=datetime(2016, 11, 1, 0, 0))  # 00:00 1/11/2016 Tuesday

    def test_next_5th_saturday_of_december(self):  # Every last Saturday of December
        """Every 5th (n=4) Saturday of December
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[5], days_of_week_num=[4], months=[12], years=None,
                        # Every 5th Saturday of December
                        current_time=datetime(2015, 10, 15, 00, 00),  # 00:00 15/10/2015 Thursday
                        expected_result=datetime(2016, 12, 31, 0, 0))  # 00:00 31/12/2016 Saturday

    def test_next_5th_wednesday(self):  # Every 5th wednesday
        """Every 5th Wednesday
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[2], days_of_week_num=[4], months=None, years=None,
                        # Every 5th Wednesday
                        current_time=datetime(2016, 10, 1, 00, 00),  # 00:00 1/10/2017 Saturday
                        expected_result=datetime(2016, 11, 30, 0, 0))  # 00:00 30/11/2016 Wednesday

    def test_next_every_even_day(self):  # Every even day at 00:00
        """Every even day at 00:00
        """
        self._test_next(minutes=[0], hours=[0], days=range(0, 31, 2), months=None, years=None,
                        # Every even day
                        current_time=datetime(2016, 11, 17, 15, 00),  # 15:00 17/11/2016 Thursday
                        expected_result=datetime(2016, 11, 18, 0, 0))  # 00:00 18/11/2016 Friday

    def test_next_every_third_hour(self):  # Every third hour
        """Every third hour
        """
        self._test_next(minutes=[0], hours=range(0, 24, 3), days=None, months=None, years=None,
                        # Every third hour
                        current_time=datetime(2016, 11, 17, 10, 00),  # 10:00 17/11/2017 Thursday
                        expected_result=datetime(2016, 11, 17, 12, 0))  # 12:00 17/11/2016 Thursday

    def test_next_monday_before_presidential_election_day(self):  # Every first Monday of November every 4rth year
        """Every first Monday of November every 4rth year, starting from 1848
        """
        self._test_next(minutes=[0], hours=[0], days_of_week=[0], days_of_week_num=[0], months=[11],
                        years=range(1848, 9999, 4),
                        # Every first Monday of November, every 4rth year starting with 1848
                        current_time=datetime(2016, 11, 17, 15, 30),  # 15:30 17/11/2016 Wednesday
                        expected_result=datetime(2020, 11, 2, 0, 0))  # 00:00 2/11/2020 Monday


if __name__ == '__main__':
    unittest.main()
