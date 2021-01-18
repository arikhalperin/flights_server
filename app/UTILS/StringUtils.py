from datetime import datetime

import dateutil
from dateutil.parser import parse


def convert_number(num):
    print(f"Converting {num}")

    if num == "one":
        return 1
    if num == "two":
        return 2
    if num == "three":
        return 3
    if num == "four":
        return 4
    if num == "five":
        return 5
    if num == "six":
        return 6
    if num == "seven":
        return 7
    if num == "eight":
        return 8
    if num == "nine":
        return 9
    if num == "ten":
        return 10
    else:
        return int(num)


def compare_date(date_to_compare, date_value):
    print(f"Extracting date:{date_value}")
    month = date_value.month
    day = date_value.day
    year = date_value.year
    date_1 = datetime(year=year, month=month, day=day)
    print(f"date1={date_1}")
    date_2 = parse(date_to_compare)
    print(f"date2={date_2}")
    return date_1.year == date_2.year and date_1.month==date_2.month and date_1.day==date_2.day
