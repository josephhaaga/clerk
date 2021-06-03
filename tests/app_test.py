import datetime
import pytest
from unittest.mock import patch

from src.app import main
from src.app import Application


TODAY = datetime.datetime.now()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TWO_DAYS_AGO = TODAY - datetime.timedelta(days=2)
FOUR_DAYS_AGO = TODAY - datetime.timedelta(days=4)
TWO_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=2)
THREE_DAYS_FROM_NOW = TODAY + datetime.timedelta(days=3)

EXAMPLE_CONFIG = {
    "DEFAULT": {
        "journal_directory": "./my-journal-directory",
        "preferred_editor": "vi",
        "date_format": "%Y-%m-%d",
        "file_extension": "md",
    }
}


@pytest.fixture(scope="session")
def example_app():
    return Application(EXAMPLE_CONFIG)


@patch("subprocess.run")
def test_application_open_file(patched_subprocess_run, example_app):
    filename = "1234.md"
    example_app.open_file(filename)
    patched_subprocess_run.assert_called_once()


@pytest.mark.parametrize(
    "date, filename",
    [
        (TODAY, f"{TODAY.strftime('%Y-%m-%d')}.md"),
        (YESTERDAY, f"{YESTERDAY.strftime('%Y-%m-%d')}.md"),
    ],
)
def test_application_convert_to_filename(date, filename, example_app):
    got = example_app.convert_to_filename(date)
    assert got == filename


def test_application_creation_fails_with_missing_config_item():
    # https://medium.com/python-pandemonium/testing-sys-exit-with-pytest-10c6e5f7726f
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        Application({"DEFAULT": {}})
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


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
@patch("src.app.Application.open_file")
def test_main_loop(patched_open_file, phrase, date):
    # mock the `get_config` with a basic config
    # patch `Application.open_file` and assert it's called as expected
    with patch("src.app.get_config", lambda: EXAMPLE_CONFIG):
        with patch("sys.argv", [" "] + phrase.split(" ")):
            main()
    patched_open_file.assert_called_once_with(f"{date}.md")
