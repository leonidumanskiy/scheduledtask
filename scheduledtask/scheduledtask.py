from datetime import datetime
from enum import Enum
from copy import copy
from .utils import get_biggest_value_less_or_equal_to, get_smallest_value_greater_or_equal_to, last, first, \
    weekday_num, weekday_and_num_to_day, num_days_in_month, weekday_and_week_to_day, week_num, max_week_num


class DateTimeHolder:
    __slots__ = ['minute', 'hour', 'day', 'day_of_week', 'day_of_week_num', 'month', 'week', 'year']

    def __init__(self, minute=None, hour=None, day=None, day_of_week=None, day_of_week_num=None, week=None,
                 month=None, year=None):
        self.minute = minute
        self.hour = hour
        self.day = day
        self.day_of_week = day_of_week
        self.day_of_week_num = day_of_week_num
        self.week = week
        self.month = month
        self.year = year

    @property
    def datetime(self):
        if self.day_of_week is not None and self.day_of_week_num is not None:
            day = weekday_and_num_to_day(self.year, self.month, self.day_of_week_num, self.day_of_week)
            return datetime(self.year, self.month, day, self.hour or 0, self.minute or 0)
        elif self.day_of_week is not None and self.week is not None:
            day = weekday_and_week_to_day(self.year, self.month, self.week, self.day_of_week)
            return datetime(self.year, self.month, day, self.hour or 0, self.minute or 0)
        else:
            return datetime(self.year, self.month or 1, self.day or 1, self.hour or 0, self.minute or 0)

    def __getitem__(self, key):
            return getattr(self, key)

    def __setitem__(self, key, value):
            return setattr(self, key, value)

    def __copy__(self):
        return DateTimeHolder(minute=self.minute, hour=self.hour, day=self.day, day_of_week=self.day_of_week,
                              day_of_week_num=self.day_of_week_num, week=self.week, month=self.month, year=self.year)

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __gt__(self, other):
        return self.datetime > other.datetime

    def __eq__(self, other):
        return self.datetime == other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime

    def __ge__(self, other):
        return self.datetime >= other.datetime


class TaskStrategy(Enum):
    days_of_month = 0  # 1-31
    days_of_week = 1  # Sun-Sat + week number
    days_of_week_num = 2  # Sun-Sat + weekday number


class DayStrategyFraction(Enum):
    minute = 0
    hour = 1
    day = 2
    month = 3
    year = 4


class DayOfWeekStrategyFraction(Enum):
    minute = 0
    hour = 1
    day_of_week = 2
    week = 3
    month = 4
    year = 5


class DayOfWeekNumStrategyFraction(Enum):
    minute = 0
    hour = 1
    day_of_week = 2
    day_of_week_num = 3
    month = 4
    year = 5


class ScheduledTask:
    def __init__(self, minutes=None, hours=None, days=None, days_of_week=None, days_of_week_num=None, weeks=None,
                 months=None, years=None, max_iterations=100):
        if days_of_week is not None and days_of_week_num is not None:
            self.strategy = TaskStrategy.days_of_week_num
            self.fractions = DayOfWeekNumStrategyFraction
            self.candidates = [minutes or range(0, 60), hours or range(0, 24), days_of_week or range(0, 7),
                               days_of_week_num or range(0, 5), months or range(1, 13), years or range(0, 9999)]

        elif days_of_week is not None or weeks is not None:
            self.strategy = TaskStrategy.days_of_week
            self.fractions = DayOfWeekStrategyFraction
            self.candidates = [minutes or range(0, 60), hours or range(0, 24), days_of_week or range(0, 7),
                               weeks or range(0, 6), months or range(1, 13), years or range(0, 9999)]

        else:
            self.strategy = TaskStrategy.days_of_month
            self.fractions = DayStrategyFraction
            self.candidates = [minutes or range(0, 60), hours or range(0, 24), days or range(1, 32),
                               months or range(1, 13), years or range(0, 9999)]

        self.highest_fraction = last([f for f in self.fractions])

        # Settings
        self.max_iterations = max_iterations

    def _datetimeholder_valid(self, datetimeholder: DateTimeHolder, fraction: Enum):
        """Check if date time holder is valid for current fraction
           i.e. if fraction is days, check if current day exists in the month
        """
        # Check min value
        if self.strategy == TaskStrategy.days_of_month:
            min_value = 1 if fraction in [self.fractions.day, self.fractions.month, self.fractions.year] else 0
        else:
            min_value = 1 if fraction in [self.fractions.month, self.fractions.year] else 0

        if datetimeholder[fraction.name] < min_value:
            return False

        # Check if day exceeds number of days in that month
        if self.strategy == TaskStrategy.days_of_month and fraction == self.fractions.day:
            n_days_in_month = num_days_in_month(datetimeholder.year, datetimeholder.month)
            if datetimeholder.day > n_days_in_month:
                return False

        # Check if day of week number exceeds number of day of weeks for this month
        if self.strategy == TaskStrategy.days_of_week_num and fraction == self.fractions.day_of_week_num:
            # Since we don't know what day of week we are validating,
            # assume that this number can't be more than max week number
            if datetimeholder.day_of_week_num > max_week_num(datetimeholder.year, datetimeholder.month):
                return False

        # Check if day of week and day of week number exceeds maximum day of week number for this month
        if self.strategy == TaskStrategy.days_of_week_num and fraction == self.fractions.day_of_week:
            day = weekday_and_num_to_day(datetimeholder.year, datetimeholder.month, datetimeholder.day_of_week_num,
                                         datetimeholder.day_of_week)
            n_days_in_month = num_days_in_month(datetimeholder.year, datetimeholder.month)
            if day > n_days_in_month:
                return False

        # Check if month has n weeks
        if self.strategy == TaskStrategy.days_of_week and fraction == self.fractions.week:
            if datetimeholder.week > max_week_num(datetimeholder.year, datetimeholder.month):
                return False

        # Check if weekday and week number combination
        if self.strategy == TaskStrategy.days_of_week and fraction == self.fractions.day_of_week:
            day = weekday_and_week_to_day(datetimeholder.year, datetimeholder.month, datetimeholder.week,
                                          datetimeholder.day_of_week)
            n_days_in_month = num_days_in_month(datetimeholder.year, datetimeholder.month)
            if day is None:
                return False
            if day > n_days_in_month:
                return False

        # All checks are passed
        return True

    def _datetimeholders_equal(self, a: DateTimeHolder, b: DateTimeHolder, from_fraction: Enum):
        """Partially check a and b date time holders for equality, starting with fraction.
           For example, if the fraction is DAY, compare only DAY, MONTH and YEAR
        """
        return all([a[self.fractions(fv).name] == b[self.fractions(fv).name] for fv
                    in range(from_fraction.value, self.highest_fraction.value+1)])

    def _datetimeholders_compare(self, a: DateTimeHolder, b: DateTimeHolder, from_fraction: Enum):
        """Partially compare a and b date time holders, starting with fraction.
           For example, if the fraction is DAY, compare only DAY, MONTH and YEAR
        """
        _a = DateTimeHolder()
        _b = DateTimeHolder()
        for fraction_value in range(from_fraction.value, self.highest_fraction.value+1):
            fraction = self.fractions(fraction_value)
            _a[fraction.name] = a[fraction.name]
            _b[fraction.name] = b[fraction.name]
        if _a > _b:
            return 1
        elif _a == _b:
            return 0
        else:
            return -1

    def _increase_fraction(self, result: DateTimeHolder, fraction: Enum, increment: int, current: DateTimeHolder):
        """Increase fraction on the datetimeholder
        :param result:Value to increase
        :param fraction:Fraction to increase
        :param current:Original value - used to reset if we can't increase
        :return:Number of fractions increased (to know from which to recalculate)
        """
        # If candidates are range, perform step-aware increment
        if type(self.candidates[fraction.value]) == list:
            new_value = result[fraction.name] + increment
        elif type(self.candidates[fraction.value]) == range:
            new_value = result[fraction.name] + increment * self.candidates[fraction.value].step
        else:
            raise ValueError("candidate must be of type list or range")

        datetimeholder_increased = copy(result)
        datetimeholder_increased[fraction.name] = new_value
        if increment > 0:  # 1
            in_range = get_smallest_value_greater_or_equal_to(self.candidates[fraction.value],
                                                          datetimeholder_increased[fraction.name]) is not None
        else:  # -1
            in_range = get_biggest_value_less_or_equal_to(self.candidates[fraction.value],
                                                          datetimeholder_increased[fraction.name]) is not None

        if self._datetimeholder_valid(datetimeholder_increased, fraction) and in_range:
            result[fraction.name] = new_value
            return 1
        else:
            if fraction == self.highest_fraction:
                raise ValueError("Can't increase fraction - current " + self.highest_fraction +
                                 " is " + result[fraction.value])
            result[fraction.name] = current[fraction.name]
            return 1 + self._increase_fraction(result, self.fractions(fraction.value + 1), increment, current)

    def get_next_time(self, current_datetime: datetime = None):
        """Returns next task execution time nearest to the given datetime
        """
        if current_datetime is None:
            current_datetime = datetime.utcnow()

        if self.strategy == TaskStrategy.days_of_month:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day=current_datetime.day, month=current_datetime.month, year=current_datetime.year)

        elif self.strategy == TaskStrategy.days_of_week:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day_of_week=current_datetime.weekday(),
                                     week=week_num(current_datetime),
                                     month=current_datetime.month, year=current_datetime.year)

        else:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day_of_week=current_datetime.weekday(),
                                     day_of_week_num=weekday_num(current_datetime),
                                     month=current_datetime.month, year=current_datetime.year)

        result = self._get_next_time(current)
        return result.datetime

    def get_previous_time(self, current_datetime: datetime = None):
        """Returns previous task execution time nearest to the given datetime
        """
        if current_datetime is None:
            current_datetime = datetime.utcnow()

        if self.strategy == TaskStrategy.days_of_month:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day=current_datetime.day, month=current_datetime.month, year=current_datetime.year)

        elif self.strategy == TaskStrategy.days_of_week:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day_of_week=current_datetime.weekday(),
                                     week=week_num(current_datetime),
                                     month=current_datetime.month, year=current_datetime.year)

        else:
            current = DateTimeHolder(minute=current_datetime.minute, hour=current_datetime.hour,
                                     day_of_week=current_datetime.weekday(),
                                     day_of_week_num=weekday_num(current_datetime),
                                     month=current_datetime.month, year=current_datetime.year)

        result = self._get_previous_time(current)
        return result.datetime

    def _get_next_time(self, current: DateTimeHolder):
        """Calculates next task time using current
        """
        result = DateTimeHolder()
        fraction_value = self.highest_fraction.value
        i = 0
        while fraction_value != -1:  # From year to minute
            i += 1
            if i > self.max_iterations:  # Max iteration check
                raise ValueError("maximum number of iterations exceeded. You found a bug with scheduledtask. Dump: " +
                                 "candidates: {}, ".format(self.candidates) +
                                 "current: {}, max_iterations: {}".format(current, self.max_iterations))

            fraction = self.fractions(fraction_value)
            if fraction is self.highest_fraction \
                    or self._datetimeholders_equal(result, current, self.fractions(fraction_value+1)):
                result[fraction.name] = get_smallest_value_greater_or_equal_to(self.candidates[fraction_value],
                                                                               current[fraction.name])
            else:
                result[fraction.name] = first(self.candidates[fraction_value])

            if result[fraction.name] is None \
                    or not self._datetimeholder_valid(result, fraction) \
                    or not self._datetimeholders_compare(result, current, fraction) > -1:  # In case with day_of_week_num
                if fraction == self.highest_fraction:
                    return None  # Can't find highest fraction match, event never happened in the past

                # Decrease higher fractions on result datetime, recalculate starting from that fraction-1
                fraction_value += self._increase_fraction(result, self.fractions(fraction_value + 1), +1, current) - 1
                continue

            fraction_value -= 1
        return result

    def _get_previous_time(self, current: DateTimeHolder):
        """Calculates previous task time using current
        """
        result = DateTimeHolder()
        fraction_value = self.highest_fraction.value
        i = 0
        while fraction_value != -1:  # From year to minute
            i += 1
            if i > self.max_iterations:  # Max iteration check
                raise ValueError("maximum number of iterations exceeded. You found a bug with scheduledtask. Dump: " +
                                 "candidates: {}, ".format(self.candidates) +
                                 "current: {}, max_iterations: {}".format(current, self.max_iterations))

            fraction = self.fractions(fraction_value)
            if fraction is self.highest_fraction \
                    or self._datetimeholders_equal(result, current, self.fractions(fraction_value + 1)):
                result[fraction.name] = get_biggest_value_less_or_equal_to(self.candidates[fraction_value],
                                                                           current[fraction.name])
            else:
                result[fraction.name] = last(self.candidates[fraction_value])

            if result[fraction.name] is None \
                    or not self._datetimeholder_valid(result, fraction) \
                    or not self._datetimeholders_compare(result, current, fraction) < 1:  # In case with day_of_week_num
                if fraction == self.highest_fraction:
                    return None  # Can't find highest fraction match, event never happened in the past

                # Decrease higher fractions on result datetime, recalculate starting from that fraction-1
                fraction_value += self._increase_fraction(result, self.fractions(fraction_value + 1), -1, current) - 1
                continue

            fraction_value -= 1
        return result
