# Move journal.sh logic into here
import datetime
import os
import pathlib
import subprocess
import sys

from src.parse import parse_english_to_date


# these should come from a config file!
HOME = os.getenv("HOME")
JOURNAL_DIRECTORY = os.getenv("PATH_TO_JOURNALS", f"{HOME}/Documents/Journal/journals")
PREFERRED_EDITOR = os.getenv("EDITOR", "vi")
DATE_FORMAT = "%Y-%m-%d"
FILE_EXTENSION = "md"


def main() -> int:
    # app configuration

    # main loop
    day = "today"  # default to today's journal
    if len(sys.argv) > 1:
        day = " ".join(sys.argv[1:])  # parse date and open that journal
    target_date = parse_english_to_date(day)
    date_as_filename = convert_to_filename(target_date)
    open_file(date_as_filename)
    return 0


def open_file(filename: str):
    file_to_open: pathlib.Path = pathlib.Path(JOURNAL_DIRECTORY, filename)
    subprocess.run([PREFERRED_EDITOR, file_to_open])
    return True


def convert_to_filename(target_date: datetime.datetime) -> str:
    """Convert a datetime.datetime object to a string 'YYYY-MM-DD'"""
    return f"{target_date.strftime(DATE_FORMAT)}.{FILE_EXTENSION}"


if __name__ == "__main__":
    exit(main())
