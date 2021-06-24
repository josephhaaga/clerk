"""Utility functions for resolving user input to dates"""
import datetime
import operator
from typing import Union

from word2number import w2n


SCALES = {
    "days": 1,
    "day": 1,
    "week": 7,
    "weeks": 7,
    "month": 30,
    "months": 30,
    "year": 365,
    "years": 365,
}

DAYS_OF_WEEK = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def parse_number(number: Union[str, int]) -> int:
    """Parse a number to an integer"""
    try:
        num = int(number)
    except ValueError:
        num = w2n.word_to_num(number)
    return num


def parse_english_to_date(english: str) -> datetime.datetime:
    """Parse an english description of a date to a datetime.datetime object"""
    query = english.strip().lower()
    today = datetime.datetime.now()
    if query == "today":
        return today
    if query == "yesterday":
        operation = operator.sub
        days = 1
    elif query == "tomorrow":
        operation = operator.add
        days = 1
    elif " ago" in query:
        operation = operator.sub
        unit, *_ = [k for k in SCALES.keys() if k in query]
        quantity = query.replace(" ago", "").replace(unit, "").strip()
        number = parse_number(quantity)
        days_in_unit = SCALES[unit]
        days = number * days_in_unit
    elif " from now" in query or " from today" in query:
        operation = operator.add
        unit, *_ = [k for k in SCALES.keys() if k in query]
        quantity = (
            query.replace(" from now", "")
            .replace(" from today", "")
            .replace(unit, "")
            .strip()
        )
        number = parse_number(quantity)
        days_in_unit = SCALES[unit]
        days = number * days_in_unit
    elif "last" in query:
        operation = operator.sub
        day = query.replace("last", "").strip()
        day_of_week = DAYS_OF_WEEK[day]
        days = 7 - (day_of_week - today.weekday())
    elif "this" in query:
        operation = operator.add
        day = query.replace("this", "").strip()
        day_of_week = DAYS_OF_WEEK[day]
        days = day_of_week - today.weekday()
    elif "next" in query:
        operation = operator.add
        day = query.replace("next", "").strip()  # tuesday
        day_of_week = DAYS_OF_WEEK[day]  # 1
        days = 7 + (day_of_week - today.weekday())
    else:
        raise ValueError(f"couldn't parse input: {english}")
    return operation(today, datetime.timedelta(days=days))
