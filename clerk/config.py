"""Utility functions for managing clerk's configuration"""
from pathlib import Path
from typing import Mapping

from appdirs import AppDirs
from configparser import ConfigParser


def dirs() -> AppDirs:
    """Returns clerk's application directories"""
    return AppDirs("clerk", "K Street Labs")


def config_file_path() -> Path:
    """Returns the path to clerk's configuration file"""
    return Path.home() / ".clerkrc"


def temp_directory_path() -> Path:
    """Returns the path to user's clerk data directory"""
    return Path(dirs().user_data_dir)


def get_config() -> Mapping:
    """Returns the configuration for the clerk application"""
    config_file = config_file_path()
    config_directory = config_file.parents[0]
    config_directory.mkdir(parents=True, exist_ok=True)
    config_file.touch(exist_ok=True)
    conf = ConfigParser()
    conf.read(config_file)
    conf["DEFAULT"]["journal_directory"] = str(
        Path(conf["DEFAULT"]["journal_directory"]).expanduser()
    )
    return conf


def write_config(conf_map: Mapping) -> None:
    """Update the clerk configuration"""
    conf_file_path = config_file_path()
    print(f"Writing to config: {conf_file_path}")
    with open(conf_file_path, "w") as configfile:
        conf_map.write(configfile)
