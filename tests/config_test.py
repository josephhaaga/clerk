"""Tests for clerk's config utility functions"""

from configparser import ConfigParser
from pathlib import Path
import pytest
from tempfile import NamedTemporaryFile
from typing import Mapping
from unittest.mock import MagicMock
from unittest.mock import patch

from clerk.config import dirs
from clerk.config import config_file_path
from clerk.config import get_config
from clerk.config import write_config


def test_dirs_contains_user_config_dir():
    """Ensure clerk.config.dirs contains user_config_dir"""
    got = dirs()
    assert isinstance(got.user_config_dir, str)


@pytest.fixture
def clerk_config():
    """Fixture to create a temporary .clerkrc for tests."""
    with patch("clerk.config.config_file_path") as patched_config_file_path:
        with NamedTemporaryFile() as f:
            with open(f.name, "w") as fs:
                fs.writelines(
                    [
                        "[DEFAULT]\n",
                        "journal_directory=~/some/journals/dir\n",
                        "preferred_editor=vi\n",
                        "date_format=%%Y-%%m-%%d\n",
                        "file_extension=md",
                    ]
                )
            patched_config_file_path.return_value = Path(f.name)
            yield


def test_get_config_returns_mapping(clerk_config):
    """Ensure clerk.config.get_config returns a Mapping object"""
    got = get_config()
    assert isinstance(got, Mapping)


@patch("pathlib.Path.expanduser")
def test_get_config_expands_journal_directory(patched_expand_user, clerk_config):
    """Ensure clerk.config.get_config expands journal_directory into an absolute path."""
    patched_expand_user.return_value = "/Users/clerk-user/some/journals/dir"
    conf = get_config()
    assert conf["DEFAULT"]["journal_directory"] == "/Users/clerk-user/some/journals/dir"


@patch("clerk.config.config_file_path")
def test_write_config_writes_successfully(patched_config_file_path):
    """Ensure clerk.config.write_config updates the config file"""
    conf = ConfigParser()
    conf["DEFAULT"]["hello"] = "hi there"
    with NamedTemporaryFile() as f:
        patched_config_file_path.return_value = Path(f.name)
        write_config(conf)
        file_contents = open(f.name, "r").readlines()
        assert file_contents == ["[DEFAULT]\n", "hello = hi there\n", "\n"]


def test_get_config_fails_with_missing_config_item():
    """Ensure application fails when a necessary configuration item is missing"""
    # https://medium.com/python-pandemonium/testing-sys-exit-with-pytest-10c6e5f7726f
    with patch("clerk.config.config_file_path") as patched_config_file_path:
        with NamedTemporaryFile() as f:
            with open(f.name, "w") as fs:
                fs.writelines(
                    [
                        "[DEFAULT]\n",
                        "file_extension=md",
                    ]
                )
            patched_config_file_path.return_value = Path(f.name)
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                get_config()
            assert pytest_wrapped_e.type == SystemExit
            assert pytest_wrapped_e.value.code == 1


# TODO: test the validation function, rather than the config file itself.
@pytest.mark.skip
@pytest.mark.parametrize(
    "field", ["journal_directory", "editor", "date_format", "file_extension"]
)
def test_config_contains_necessary_fields(field):
    """Ensure that the config file contains the necessary fields"""
    config = get_config()
    assert field in config
