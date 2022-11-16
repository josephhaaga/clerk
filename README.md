# clerk

![Interrogate docstring coverage](./docs/_static/interrogate-badge.svg)
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

## Installation

```
$ pipx install josephhaaga-clerk && pipx ensurepath
```

## Setup

Create a `.clerkrc` file in your home directory that looks like the following, but fill in your own details. For example, [here's mine](https://github.com/josephhaaga/dotfiles/blob/master/.clerkrc)!

```
[DEFAULT]
journal_directory=~/journals  # where your journals will be created
preferred_editor=vi  # or code, nano, emacs, babi
date_format=%%Y-%%m-%%d  # double % required - used in datetime's strftime()
file_extension=md  # or rst, txt
```

*Note: ini files don't support comments; remove those!*



### Hooks

As of v0.0.2, you can add custom callback functions. Simply add the callback name in your `.clerkrc`, and ensure the package is installed!

For example, here's how you'd configure [clerk-timestamp](https://github.com/josephhaaga/clerk-timestamp) to fire every time you open a journal

```
[DEFAULT]
...

[hooks]
JOURNAL_OPENED =
    timestamp
```

Callback-specific configuration can be provided in a separate block in your `.clerkrc` config file (see [clerk-timestamp example](https://github.com/josephhaaga/clerk-timestamp#configuration))

#### Custom Callback functions

Callback functions receive the entire journal document as a list of lines `List[str]`, and can return their own `List[str]` of lines that will overwrite the document. (`return None` or `False` if you don't wish to make any changes)

Note that callback functions are called in the order they're listed, so in the following configuration, will receive the output of the first callback function. In the following example, `timestamp` receives the output of `fortune-cookie`

```
[DEFAULT]
...

[hooks]
NEW_JOURNAL_CREATED =
    fortune-cookie
    timestamp
```


#### Available Hooks

All hooks have the following interface

**Input**:
* a `Sequence[str]` representing the lines in the journal document
* a `Mapping` containing any user-provided configuration

**Output**: a `List[str]` representing the updated journal document (returning `None` or `False` will prevent any update)


##### New journal created

The `NEW_JOURNAL_CREATED` hook runs whenever the user opens a journal file that does not exist yet.

##### Journal opened

The `JOURNAL_OPENED` hook runs whenever the user opens a journal file.

##### Journal saved

The `JOURNAL_SAVED` hook runs whenever a user saves their journal (resulting in the file's `md5` hash changing).

##### Journal closed

The `JOURNAL_CLOSED` hook runs whenever a user closes their journal.
