import datetime
import operator
from typing import Union

from word2number import w2n


scales = {
    "days": 1,
    "day": 1,
    "week": 7,
    "weeks": 7,
    "month": 30,
    "months": 30,
    "year": 365,
    "years": 365,
}


def parse_number(number: Union[str, int]) -> int:
    try:
        num = int(number)
    except ValueError:
        num = w2n.word_to_num(number)
    return num


def parse_english_to_date(english: str) -> datetime.datetime:
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
        unit, *_ = [k for k in scales.keys() if k in query]
        quantity = query.replace(" ago", "").replace(unit, "").strip()
        number = parse_number(quantity)
        days_in_unit = scales[unit]
        days = number * days_in_unit
    elif " from now" or " from today" in query:
        operation = operator.add
        unit, *_ = [k for k in scales.keys() if k in query]
        quantity = (
            query.replace(" from now", "")
            .replace(" from today", "")
            .replace(unit, "")
            .strip()
        )
        number = parse_number(quantity)
        days_in_unit = scales[unit]
        days = number * days_in_unit
    # TODO else: raise Exception
    return operation(today, datetime.timedelta(days=days))


#   else if query.startswith("last"):
#       pass
#   else if query.startswith("next"):
#
