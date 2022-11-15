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


def test_get_config_returns_mapping():
    """Ensure clerk.config.get_config returns a Mapping object"""
    got = get_config()
    assert isinstance(got, Mapping)


@patch("pathlib.Path.expanduser")
@patch("clerk.config.config_file_path")
def test_get_config_expands_journal_directory(patched_config_file_path, patched_expand_user):
    """Ensure clerk.config.get_config expands journal_directory into an absolute path."""
    patched_expand_user.return_value = "/Users/clerk-user"
    with NamedTemporaryFile() as f:
        with open(f.name, "w") as fs:
            fs.write("[DEFAULT]\njournal_directory=~/some/journals/dir")
        patched_config_file_path.return_value = Path(f.name)
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


@pytest.mark.skip
@pytest.mark.parametrize(
    "field", ["journal_directory", "editor", "date_format", "file_extension"]
)
def test_config_contains_necessary_fields(field):
    """Ensure that the config file contains the necessary fields"""
    config = get_config()
    assert field in config
