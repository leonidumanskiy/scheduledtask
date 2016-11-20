Copyright 2016 Leonid Umanskiy

Released under MIT license

[![Build Status](https://travis-ci.org/leonidumanskiy/scheduledtask.svg?branch=master)](https://travis-ci.org/leonidumanskiy/scheduledtask)

# Description
This package provides functionality to work with scheduled tasks (cron-alike) in Python.
The main intention is to let you use planned scheduled tasks in lazy environments, 
like web server, by providing functions to check previous and next execution time of the task (**get_previous_time** and **get_next_time**).

This package doesn't parse cron string and is not fully compatible with cron. 
It currently doesn't support last day of month and last weekday functionality, 
however it supports providing day of week number (#) or providing a week number.
Rules can be provided in a form of list of integers, range (step will be counted), or None.

# Installation
```
pip install scheduledtask
```

# Quick start
####Task that executes twice a day: at 00:00 and 00:30, get next execution time
```python
from scheduledtask import ScheduledTask

task = ScheduledTask(minutes=[0, 30], hours=[0], days=None, months=None, years=None)
print(task.get_next_time())
```

####Task that executes every 1st day of Month
```python
from scheduledtask import ScheduledTask
from datetime import datetime

task = ScheduledTask(minutes=[0], hours=[0], days=[1], months=None, years=None)
print(task.get_previous_time(current_datetime=datetime(2016, 11, 19))  
# Prints datetime(2016, 12, 1, 0, 0))
```

####More complex example:
Get next and previous USA presidential election day by getting the next day after first monday of November every 4rth year
```python
from scheduledtask import ScheduledTask

task = ScheduledTask(minutes=[0], hours=[0], days_of_week=[0], days_of_week_num=[0], months=[11], 
                     years=range(1848, 9999, 4))
print(task.get_next_time() + timedelta(days=1))
print(task.get_previous_time() + timedelta(days=1))
```

# Rules

#### Rule types
When creating a ScheduledTask object, you can provide rules of when this task must be executed.
Every rule can be of 3 types:
- **list**: List of values. List can contain 1 value.
- **range**: Range of values, might contain valid step. For example, day=range(2, 31, 2) means "every even day of month".
- **None**: None means every valid value (* in cron).

#### Rule fields
| Field            | Value  | Strategies                      | Description                                                                            |
|------------------|--------|---------------------------------|----------------------------------------------------------------------------------------|
| minutes          | 0-59   | *                               | Minutes                                                                                |
| hours            | 0-23   | *                               | Hours                                                                                  |
| days             | 1-31   | days_of_month                   | Days                                                                                   |
| days_of_week     | 0-6    | days_of_week,  days_of_week_num | Days of week - Monday to Sunday                                                        |
| days_of_week_num | 0-4    | days_of_week_num                | Number of day of week. For example, 0 and Friday means every 1st Friday of a month     |
| weeks            | 0-5    | days_of_week                    | Week number. 0 and Friday means every Friday that happens in the first week of a month |
| months           | 1-12   | *                               | Months                                                                                 |
| years            | 0-9999 | *                               | Years                                                                                  |

#### Strategies
When creating a ScheduledTask, not all fields are compatible with each other.
Generally, there are 3 strategies that will be used:
- **days_of_month** - default strategy. Used if **days** rule is provided and non of week-related rules are provided. 
- **days_of_week** - this strategy is chosen when **days_of_week** and/or **weeks** rules are provided. If that strategy is chosen, **days** or **days_of_week_num** rules are ignored. 
- **days_of_week_num** - this strategy is chosen when **days_of_week** and **days_of_week_num** rules are provided. This is used to set up rules like "2nd Monday of July".

# Providing current time
When calling **get_previous_time** or **get_next_time**, you can provide **current_datetime** to check against. 
If no current datetime is provided, datetime.utcnow() will be used. 
**current_datetime** doesn't have to be in UTC-format. This library is timezone-agnostic and will return result using the same timezone as current_datetime.

