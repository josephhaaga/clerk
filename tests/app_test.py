"""Test clerk main application logic"""
import datetime
import pathlib
import pytest
import tempfile
from unittest.mock import patch, MagicMock

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
def journal_dir():
    """Fixture to set up journal_directory."""
    with tempfile.TemporaryDirectory() as t:
        yield t


@pytest.fixture(scope="session")
def example_app(user_data_dir, journal_dir):
    """Fixture to set up an application object"""
    c = EXAMPLE_CONFIG
    c["DEFAULT"]["journal_directory"] = journal_dir
    yield Application(c, user_data_dir, {})


@patch("subprocess.run")
def test_application_open_journal(patched_subprocess_run, example_app):
    """Ensure Application.open_journal calls subprocess.run"""
    filename = "1234.md"
    example_app.open_journal(filename)
    patched_subprocess_run.assert_called_once()


def test_application_quits_on_missing_journals_dir():
    """Ensure Application raises a SystemExit when the journal_directory doesn't exist."""
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        with tempfile.TemporaryDirectory() as d:
            tmp_config = {
                "DEFAULT": {
                    "journal_directory": f"{d}/some-nonexistent-directory",
                    "preferred_editor": "vi",
                    "date_format": "%Y-%m-%d",
                    "file_extension": "md",
                }
            }
            Application(tmp_config, user_data_dir, {})
    assert pytest_wrapped_e.type == FileNotFoundError


def test_application_wont_open_duplicate(user_data_dir, example_app):
    """Ensure Application.open_journal wont open multiple copies of a file concurrently."""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with tempfile.NamedTemporaryFile(dir=example_app.temp_directory) as t:
            example_app.open_journal(t.name)
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


@patch("subprocess.run")
def test_journal_closed_changes_get_applied(patched_subprocess_run, example_app):
    """Ensure the JOURNAL_CLOSED hook is applied to the final output file."""
    m = MagicMock(return_value=["HELLO WORLD"])
    custom_hook_implementation = MagicMock()
    custom_hook_implementation.name = "custom"
    custom_hook_implementation.load.return_value = m
    example_app.hooks["JOURNAL_CLOSED"] = [custom_hook_implementation]
    with tempfile.NamedTemporaryFile(dir=example_app.journal_directory) as t:
        filename = pathlib.Path(t.name).name
        example_app.open_journal(filename)
        m.assert_called_once()
        with open(t.name, "r") as f:
            assert f.readlines() == ["HELLO WORLD"]
