import datetime
import pytest
from unittest.mock import patch

from src.parse import parse_english_to_date


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)

WEDNESDAY = 3
_til_next_wednesday = (WEDNESDAY - TODAY.weekday()) % 7
NEXT_WEDNESDAY = TODAY - datetime.timedelta(days=_til_next_wednesday)

LAST_WEDNESDAY = None


@pytest.mark.parametrize(
    "english, expected",
    [
        ("today", TODAY),
        ("yesterday", YESTERDAY),
        ("2 days ago", TWO_DAYS_AGO),
        ("four days ago", FOUR_DAYS_AGO),
        ("two days from now", TWO_DAYS_FROM_NOW),
        ("3 days from now", THREE_DAYS_FROM_NOW),
    ],
)
def test_parse_english_to_date(english, expected):
    got = parse_english_to_date(english)
    got = (got.year, got.month, got.day)
    expectation = (expected.year, expected.month, expected.day)
    assert got == expectation


@pytest.mark.parametrize(
    "today, english, expected",
    [
        (
            datetime.datetime.fromisocalendar(2021, 1, 1),
            "this wednesday",
            datetime.datetime.fromisocalendar(2021, 1, 3),
        ),
        (
            datetime.datetime.fromisocalendar(2021, 1, 1),
            "next wednesday",
            datetime.datetime.fromisocalendar(2021, 2, 3),
        ),
        (
            datetime.datetime.fromisocalendar(2021, 2, 1),
            "last wednesday",
            datetime.datetime.fromisocalendar(2021, 1, 3),
        ),
    ],
)
def test_parse_english_to_date_last_next_this(today, english, expected):
    with patch("datetime.datetime") as patched_datetime:
        patched_datetime.now.return_value = expected
        got = parse_english_to_date(english)
        got = (got.year, got.month, got.day)
        expectation = (expected.year, expected.month, expected.day)
        assert got == expectation
