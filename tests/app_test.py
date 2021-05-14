import datetime

import pytest

from my_journal.app import parse_english_to_date


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
LAST_WEDNESDAY = None

@pytest.mark.parametrize("english, expected", [
    ("yesterday", YESTERDAY),
    ("2 days ago", TWO_DAYS_AGO),
    ("four days ago", FOUR_DAYS_AGO),
    ("last wednesday", LAST_WEDNESDAY),
])
def test_parse_english_to_date(english, expected):
    assert parse_english_to_date(english) == expected
