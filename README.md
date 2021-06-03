# clerk

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/josephhaaga/clerk/main.svg)](https://results.pre-commit.ci/latest/github/josephhaaga/clerk/main)

Simple CLI to create new Markdown journal entry files.

## Usage
```bash
$ journal
# Creates or re-opens today's journal

$ journal tomorrow
# Creates or re-opens tomorrow's journal

$ journal last friday
# Creates or re-opens last friday's journal
```

## Setup

You'll need a config like the following

```
[DEFAULT]
journal_directory=/Users/josephhaaga/journals  # absolute path
preferred_editor=vi  # or code, nano, emacs, babi
date_format=%%Y-%%m-%%d  # double % required - used in datetime's strftime()
file_extension=md  # or rst, txt
```
