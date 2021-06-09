# Move journal.sh logic into here
import datetime
import os
import pathlib
import subprocess
import sys
from typing import Mapping

from src.clerk.config import config_file_path
from src.clerk.config import get_config
from src.clerk.parse import parse_english_to_date


def main() -> int:
    # app configuration
    config = get_config()
    app = Application(config)

    # main loop
    day = "today"  # default to today's journal
    if len(sys.argv) > 1:
        day = " ".join(sys.argv[1:])  # parse date and open that journal
    target_date = parse_english_to_date(day)
    date_as_filename = app.convert_to_filename(target_date)
    app.open_file(date_as_filename)
    return 0


class Application:
    def __init__(self, config: Mapping):
        # try to read config, and ensure required values are present
        # TODO: otherwise, instruct user to setup their config file (`clerk configure`)
        try:
            self.journal_directory = config["DEFAULT"]["journal_directory"]
            self.preferred_editor = config["DEFAULT"]["preferred_editor"]
            self.date_format = config["DEFAULT"]["date_format"]
            self.file_extension = config["DEFAULT"]["file_extension"]
        except KeyError as e:
            print(
                f"Your configuration at {config_file_path()} is missing a key '{e.args[0]}'"
            )
            exit(1)

    def open_file(self, filename: str):
        file_to_open: pathlib.Path = pathlib.Path(self.journal_directory, filename)
        subprocess.run([self.preferred_editor, file_to_open])
        return True

    def convert_to_filename(self, target_date: datetime.datetime) -> str:
        """Convert a datetime.datetime object to a string 'YYYY-MM-DD'"""
        return f"{target_date.strftime(self.date_format)}.{self.file_extension}"


if __name__ == "__main__":
    exit(main())
