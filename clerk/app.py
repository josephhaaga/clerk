import datetime
import os
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Mapping

from clerk.config import config_file_path
from clerk.config import get_config
from clerk.parse import parse_english_to_date


def main() -> int:
    config = get_config()
    app = Application(config)

    # main loop
    day = "today"  # default to today's journal
    if len(sys.argv) > 1:
        day = " ".join(sys.argv[1:])  # parse date and open that journal
    target_date = parse_english_to_date(day)
    date_as_filename = app.convert_to_filename(target_date)
    app.open_journal(date_as_filename)
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

    def open_journal(self, filename: str):
        file_to_open: pathlib.Path = pathlib.Path(self.journal_directory, filename)
        with tempfile.NamedTemporaryFile() as journal:
            if not pathlib.Path(file_to_open).exists():
                print("NEW_JOURNAL_CREATED")
            else:
                shutil.copy(file_to_open, journal.name)

            old_hash = get_file_hash(journal.name)

            print("JOURNAL_OPENED")
            subprocess.run([self.preferred_editor, journal.name])

            new_hash = get_file_hash(journal.name)

            if old_hash != new_hash:
                print("JOURNAL_SAVED")
                shutil.copy(journal.name, file_to_open)

            print("JOURNAL_CLOSED")
            return True

    def convert_to_filename(self, target_date: datetime.datetime) -> str:
        """Convert a datetime.datetime object to a string 'YYYY-MM-DD'"""
        return f"{target_date.strftime(self.date_format)}.{self.file_extension}"


def get_file_hash(filename):
    with open(filename, "r") as f:
        return hashlib.md5(f.read().encode("utf-8")).hexdigest()


if __name__ == "__main__":
    exit(main())
