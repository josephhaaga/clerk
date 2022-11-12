"""Main application logic"""
import datetime
import os
import hashlib
import importlib.metadata
import pathlib
import shutil
import subprocess
import sys
from typing import Callable
from typing import Sequence
from typing import Mapping

from clerk.config import config_file_path
from clerk.config import temp_directory_path
from clerk.config import get_config
from clerk.parse import parse_english_to_date


def main() -> int:
    """Main application entrypoint"""
    try:
        eps = importlib.metadata.entry_points()["clerk.extensions"]
        # https://youtu.be/fY3Y_xPKWNA?t=717
        _extensions = {entrypoint.name: entrypoint for entrypoint in eps}
    except KeyError:
        # no plugins installed
        _extensions = {}

    config = get_config()
    user_data_directory = temp_directory_path
    app = Application(config, user_data_directory, _extensions)

    # main loop
    day = "today"  # default to today's journal
    if len(sys.argv) > 1:
        day = " ".join(sys.argv[1:])  # parse date and open that journal
    target_date = parse_english_to_date(day)
    date_as_filename = app.convert_to_filename(target_date)
    app.open_journal(date_as_filename)
    return 0


class Application:
    """Application class"""

    def __init__(
        self, config: Mapping, user_data_directory: pathlib.Path, extensions: Mapping
    ):
        """Initialize a clerk Application object"""
        # try to read config, and ensure required values are present
        # TODO: otherwise, instruct user to setup their config file (`clerk configure`)
        try:
            self.config = config
            self.extensions = extensions
            self.temp_directory = user_data_directory
            self.journal_directory = self.config["DEFAULT"]["journal_directory"]
            self.preferred_editor = self.config["DEFAULT"]["preferred_editor"]
            self.date_format = self.config["DEFAULT"]["date_format"]
            self.file_extension = self.config["DEFAULT"]["file_extension"]
            self.hooks = {
                "NEW_JOURNAL_CREATED": self._get_callbacks_for_hook(
                    "NEW_JOURNAL_CREATED"
                ),
                "JOURNAL_OPENED": self._get_callbacks_for_hook("JOURNAL_OPENED"),
                "JOURNAL_SAVED": self._get_callbacks_for_hook("JOURNAL_SAVED"),
                "JOURNAL_CLOSED": self._get_callbacks_for_hook("JOURNAL_CLOSED"),
            }
        except KeyError as e:
            print(
                f"Your configuration at {config_file_path()} is missing a key '{e.args[0]}'"
            )
            exit(1)

    def _get_callbacks_for_hook(self, hook_name: str) -> Sequence[Callable]:
        """Gather callback functions for a specified hook"""
        if "hooks" not in self.config:
            return []
        if hook_name not in self.config["hooks"]:
            return []
        try:
            return [
                self.extensions[ext_name]
                for ext_name in self.config["hooks"][hook_name].split("\n")
                if ext_name != ""
            ]
        except KeyError as e:
            print(
                f"Couldn't find plugin '{e.args[0]}' installed; please check your configuration at {config_file_path()}"
            )
            exit(1)

    def _apply_callbacks_for_hook(self, hook_name: str, filename: pathlib.Path):
        """Apply the callbacks for a specified hook to a specified file"""
        with open(filename, "r+") as f:
            for callback in self.hooks[hook_name]:
                f.seek(0)
                data = f.readlines()
                conf = (
                    self.config[callback.name] if callback.name in self.config else {}
                )
                results = callback.load()(data, conf)
                if results:
                    f.seek(0)
                    f.writelines(results)
                    print(f"{callback.name} ran; changes applied!")
                else:
                    print(f"{callback.name} ran; no changes made")
                f.truncate()

    def open_journal(self, filename: str):
        """Opens the specified journal for writing, calling appropriate Hooks along the way, and handles eventual write or discard."""
        file_to_open: pathlib.Path = pathlib.Path(self.journal_directory, filename)
        temporary_copy: pathlib.Path = pathlib.Path(self.temp_directory, filename)
        if temporary_copy.exists():
            print("File already open!")
            exit(1)
        else:
            f = open(temporary_copy, "a")
            f.write("")
            f.close()
        if not pathlib.Path(file_to_open).exists():
            self._apply_callbacks_for_hook("NEW_JOURNAL_CREATED", temporary_copy)
        else:
            shutil.copy(file_to_open, temporary_copy)

        self._apply_callbacks_for_hook("JOURNAL_OPENED", temporary_copy)

        old_hash = get_file_hash(temporary_copy)
        subprocess.run([self.preferred_editor, temporary_copy])
        new_hash = get_file_hash(temporary_copy)

        if old_hash != new_hash:
            self._apply_callbacks_for_hook("JOURNAL_SAVED", temporary_copy)
            shutil.copy(temporary_copy, file_to_open)

        self._apply_callbacks_for_hook("JOURNAL_CLOSED", temporary_copy)
        temporary_copy.unlink()  # delete temp copy
        return True

    def convert_to_filename(self, target_date: datetime.datetime) -> str:
        """Convert a datetime.datetime object to a string 'YYYY-MM-DD'"""
        return f"{target_date.strftime(self.date_format)}.{self.file_extension}"


def get_file_hash(filename: str):
    """Return the md5 hash of a file's contents"""
    with open(filename, "r") as f:
        return hashlib.md5(f.read().encode("utf-8")).hexdigest()


if __name__ == "__main__":
    exit(main())
