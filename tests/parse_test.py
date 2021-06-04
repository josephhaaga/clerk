import datetime
import pytest
from unittest.mock import patch

from src.parse import parse_english_to_date
from src import parse


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)


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
    "todays_date, english, expected_date",
    [
        ("2021-01-04", "this wednesday", "2021-01-06"),
        ("2021-01-04", "this tuesday", "2021-01-05"),
        ("2021-01-06", "this monday", "2021-01-04"),
        # ("2021-01-04", "next wednesday", "2021-01-13"),
        ("2021-01-11", "last monday", "2021-01-04"),
        ("2021-01-11", "last wednesday", "2021-01-06"),
        ("2021-01-11", "last thursday", "2021-01-07"),
    ],
)
def test_parse_english_to_date_last_next_this(todays_date, english, expected_date):
    today = datetime.datetime.fromisoformat(todays_date)
    with patch("datetime.datetime") as patched_datetime:
        patched_datetime.now.return_value = today
        got = parse_english_to_date(english)
        got = (got.year, got.month, got.day)
    _d = datetime.datetime.fromisoformat(expected_date)
    expectation = (_d.year, _d.month, _d.day)
    assert got == expectation
