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
    got = dirs()
    assert isinstance(got.user_config_dir, str)


def test_config_file_path_contains_clerk_dot_conf():
    got = config_file_path()
    assert "clerk.conf" == str(got)[-10:]


def test_get_config_returns_mapping():
    got = get_config()
    assert isinstance(got, Mapping)


@patch("clerk.config.config_file_path")
def test_write_config_writes_successfully(patched_config_file_path):
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
    config = get_config()
    assert field in config
