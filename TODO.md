# Todos

- [X] create basic workflow to open appropriate journal files
- [X] test the main application loop (`app.main()`)
- [X] add basic config file handling
- [X] add "next tuesday" and "last thursday" functionality to parse.py
- [ ] add "create new journal" functionality with a sensible templating solution
    - add prehook and posthook functionality around the `subprocess.run` call
        - then add a custom prehook that, if file is new, inserts a rendered template
- [ ] add a `clerk` console script that uses argparse
    - `clerk --config` should return the path to the config file
    - `clerk configure` should open the config file in an editor
        - unless the user doesn't have an editor specified
    - `clerk stats` could return some other stuff
    - `clerk <pluginname>` could be a dedicated entrypoint for plugins?
        - `clerk hyperthymestic` could run a search? or update the db?
- [ ] add Google Tasks API integration
    - add a config option/flag to seed new journals with Google Tasks
    - a config option to update Google Tasks whenever I save my journal
        - maybe config file hooks for `on_create`, `on_open`, `on_save` and `on_discard`?
- [ ] add an error log in the appdir
- [ ] publish package
    - create a `console_scripts` "alias" for `journal`
    - setup.cfg, pyproject.toml
- [ ] create a `clerk-extension` starter template repo, with documentation on how to publish

## Hooks functionality
- [X] add hooks functionality to main function
- [X] update config to parse hook specifications from config files
- [X] figure out how hooks get installed
- [X] write a simple hook to append a timestamp
- Will 0.0.2 automatically read the 0.0.2/clerk.conf file? Build the package, make a new virtualenv, and install to find out


## More extensions
- use `cowsay` to print cow, dinosaur etc.
- use cowsay to print google tasks
- blackendocs to blacken any python snippets
- autosave, which will copy the tempfile back even if I don't save from my text editor
- fortune cookie, which adds a fortune to your journal
- forecast, adds weather to your journal

## Misc
- add `file_extension` suffix to tempfile so `vi` will render markdown correctly
