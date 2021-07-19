"""Test clerk main application logic"""
import datetime
import pathlib
import pytest
import tempfile
from unittest.mock import patch

from clerk.app import main
from clerk.app import Application


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
def user_data_dir():
    """Fixture to set up user data directory."""
    with tempfile.TemporaryDirectory() as t:
        yield t


@pytest.fixture(scope="session")
def example_app(user_data_dir):
    """Fixture to set up an application object"""
    return Application(EXAMPLE_CONFIG, user_data_dir, {})


@patch("subprocess.run")
def test_application_open_journal(patched_subprocess_run, example_app):
    """Ensure Application.open_journal calls subprocess.run"""
    with tempfile.TemporaryDirectory() as some_dir:
        filename = "1234.md"
        existing_journal = pathlib.Path(some_dir, filename)
        f = open(existing_journal, "a")
        f.write("Now the file has more content!")
        f.close()
        example_app.open_journal(filename)
    patched_subprocess_run.assert_called_once()


def test_application_wont_open_duplicate(user_data_dir, example_app):
    """Ensure Application.open_journal wont open multiple copies of a file concurrently."""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        filename = "12345.md"
        existing_journal = pathlib.Path(user_data_dir, filename)
        f = open(existing_journal, "a")
        f.write("Now the file has more content!")
        f.close()
        example_app.open_journal(filename)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@pytest.mark.parametrize(
    "date, filename",
    [
        (TODAY, f"{TODAY.strftime('%Y-%m-%d')}.md"),
        (YESTERDAY, f"{YESTERDAY.strftime('%Y-%m-%d')}.md"),
    ],
)
def test_application_convert_to_filename(date, filename, example_app):
    """Ensure Application.convert_to_filename converts a datetime.datetime to expected filename"""
    got = example_app.convert_to_filename(date)
    assert got == filename


def test_application_creation_fails_with_missing_config_item(user_data_dir):
    """Ensure application fails when a necessary configuration item is missing"""
    # https://medium.com/python-pandemonium/testing-sys-exit-with-pytest-10c6e5f7726f
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        Application({"DEFAULT": {}}, user_data_dir, {})
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@pytest.mark.parametrize(
    "phrase,date",
    [
        ("today", TODAY.strftime("%Y-%m-%d")),
        ("yesterday", YESTERDAY.strftime("%Y-%m-%d")),
        ("two days ago", TWO_DAYS_AGO.strftime("%Y-%m-%d")),
        ("2 days ago", TWO_DAYS_AGO.strftime("%Y-%m-%d")),
        ("four days ago", FOUR_DAYS_AGO.strftime("%Y-%m-%d")),
        ("two days from now", TWO_DAYS_FROM_NOW.strftime("%Y-%m-%d")),
        ("three days from now", THREE_DAYS_FROM_NOW.strftime("%Y-%m-%d")),
    ],
)
@patch("clerk.app.Application.open_journal")
def test_main_loop(patched_open_journal, phrase, date):
    """Ensure the main entrypoint calls Application.open_journal with the expected filename"""
    # mock the `get_config` with a basic config
    # patch `Application.open_journal` and assert it's called as expected
    with patch("clerk.app.get_config", lambda: EXAMPLE_CONFIG):
        with patch("sys.argv", [" "] + phrase.split(" ")):
            main()
    patched_open_journal.assert_called_once_with(f"{date}.md")
