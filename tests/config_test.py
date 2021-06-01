from typing import Mapping

from src.config import dirs
from src.config import config_file_path
from src.config import get_config


def test_dirs_contains_user_config_dir():
    got = dirs()
    assert isinstance(got.user_config_dir, str)


def test_config_file_path_contains_clerk_dot_conf():
    got = config_file_path()
    assert "clerk.conf" == str(got)[-10:]


def test_get_config_returns_mapping():
    got = get_config()
    assert isinstance(got, Mapping)
