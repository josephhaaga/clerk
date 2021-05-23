import datetime

import pytest

from clerk.parse import parse_english_to_date


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)
LAST_WEDNESDAY = None


@pytest.mark.parametrize(
    "english, expected",
    [
        ("today", TODAY),
        ("yesterday", YESTERDAY),
        ("2 days ago", TWO_DAYS_AGO),
        ("four days ago", FOUR_DAYS_AGO),
        ("two days from now", TWO_DAYS_FROM_NOW),
        ("3 days from now", THREE_DAYS_FROM_NOW)
        #    ("last wednesday", LAST_WEDNESDAY),
    ],
)
def test_parse_english_to_date(english, expected):
    got = parse_english_to_date(english)
    got = (got.year, got.month, got.day)
    expectation = (expected.year, expected.month, expected.day)
    assert got == expectation
