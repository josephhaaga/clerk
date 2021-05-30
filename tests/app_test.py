import datetime
import pytest
from unittest.mock import patch

from src.app import main


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)
LAST_WEDNESDAY = None


@pytest.mark.parametrize("phrase,date", [("yesterday",), ()])
@patch("subprocess.run")
def test_main(subprocess_run):
    main()
    breakpoint()
    assert subprocess_run.called_with()
