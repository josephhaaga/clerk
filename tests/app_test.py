import datetime
import pytest
from unittest.mock import patch

from src import app


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)


@pytest.mark.parametrize(
    "phrase,date",
    [
        ("today", TODAY.strftime("%Y-%m-%d")),
        ("yesterday", YESTERDAY.strftime("%Y-%m-%d")),
        ("two days ago", TWO_DAYS_AGO.strftime("%Y-%m-%d")),
        ("four days ago", FOUR_DAYS_AGO.strftime("%Y-%m-%d")),
        ("two days from now", TWO_DAYS_FROM_NOW.strftime("%Y-%m-%d")),
        ("three days from now", THREE_DAYS_FROM_NOW.strftime("%Y-%m-%d")),
    ],
)
@patch("src.app.open_file")
def test_main(patched_open_file, phrase, date):
    with patch("sys.argv", [" "] + phrase.split(" ")):
        app.main()
    patched_open_file.assert_called_once_with(f"{date}.md")
