from pathlib import Path
from typing import Mapping

from appdirs import AppDirs
from configparser import ConfigParser

from src import __version__


def dirs() -> AppDirs:
    return AppDirs("clerk", "K Street Labs", version=__version__)


def config_file_path() -> Path:
    return Path(dirs().user_config_dir) / "clerk.conf"


def get_config() -> Mapping:
    config_file = config_file_path()
    config_directory = config_file.parents[0]
    config_directory.mkdir(parents=True, exist_ok=True)
    config_file.touch(exist_ok=True)
    conf = ConfigParser()
    conf.read(config_file)
    return conf


def write_config(conf_map: Mapping) -> None:
    conf_file_path = config_file_path()
    print(f"Writing to config: {conf_file_path}")
    with open(conf_file_path, "w") as configfile:
        conf_map.write(configfile)
