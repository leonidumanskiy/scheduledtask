from datetime import datetime
from calendar import monthrange


def get_biggest_value_less_or_equal_to(iter: list or range, value):
    """Returns the biggest element from the list that is less or equal to the value. Return None if not found
    """
    if type(iter) == list:
        i = [x for x in iter if x <= value]
        return max(i) if i else None

    elif type(iter) == range:
        if value in range(iter.start, iter.stop):  # Value lies within this range, return step-aware value
            return value - ((value - iter.start) % iter.step)
        elif value > iter.stop-1:  # value is greater than range, return last element of range
            return iter.stop-1
        else:  # value is less than range, return None
            return None

    else:
        raise ValueError("iter must be of type list or range")


def get_smallest_value_greater_or_equal_to(iter: list or range, value):
    """Returns the smallest element from the list that is greater or equal to the value. Return None if not found
    """
    if type(iter) == list:
        i = [x for x in iter if x >= value]
        return min(i) if i else None

    elif type(iter) == range:
        if value in range(iter.start, iter.stop):  # Value lies within this range, return step-aware value
            return value + (iter.step - ((value - iter.start) % iter.step)) % iter.step
        elif value < iter.start:  # Value is less than range start, return start
            return iter.start
        else:  # Value is greater than range, return None
            return None

    else:
        raise ValueError("iter must be of type list or range")


def last(iter: list or range):
    """Returns the last element from the list or range
    """
    if type(iter) == list:
        return iter[len(iter)-1]
    elif type(iter) == range:
        return iter.stop - (iter.stop - 1 - iter.start) % iter.step - 1  # Step-aware last element
    else:
        raise ValueError("iter must be of type list or range")


def first(iter: list or range):
    """Returns first element from the list or range
    """
    if type(iter) == list:
        return iter[0]
    elif type(iter) == range:
        return iter.start
    else:
        raise ValueError("iter must be of type list or range")


def num_days_in_month(year: int, month: int):
    return monthrange(year, month)[1]


def weekday_num(dt: datetime):
    """Returns number of weekday in the current month. I.e. if Tuesday is first in this month, returns 0
    """
    return int((dt.day - 1)/7)


def weekday_and_num_to_day(year: int, month: int, weekday_number: int, weekday: int):
    """Converts current year, month, weekday and weekday number into the day of month
    """
    dt_first = datetime(year, month, 1)
    dt_first_weekday = dt_first.weekday()
    return 1 - dt_first_weekday + weekday + ((0 if weekday >= dt_first_weekday else 1) + weekday_number) * 7


def weekday_and_week_to_day(year: int, month: int, week: int, weekday: int):
    """Converts current year, month, weekday and week number into the day of month
    """
    dt_first = datetime(year, month, 1)
    dt_first_weekday = dt_first.weekday()
    result = week * 7 + weekday - dt_first_weekday + 1
    if result < 1 or result > num_days_in_month(year, month):
        return None
    else:
        return result


def week_num(dt: datetime):
    """Returns week number of the given day
    """
    dt_first = dt.replace(day=1)
    dt_first_weekday = dt_first.weekday()
    return int((dt.day + dt_first_weekday - 1) / 7)


def max_week_num(year: int, month: int):
    """Returns number of weeks (Monday to Friday) that month contains
    """
    # The same thing as week number for the last day of month
    return week_num(datetime(year, month, num_days_in_month(year, month)))
