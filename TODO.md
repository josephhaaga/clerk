# Todos

- [X] create basic workflow to open appropriate journal files
- [X] test the main application loop (`app.main()`)
- [X] add basic config file handling
- [X] add "next tuesday" and "last thursday" functionality to parse.py
- [ ] add "create new journal" functionality with a sensible templating solution
    - add prehook and posthook functionality around the `subprocess.run` call
        - then add a custom prehook that, if file is new, inserts a rendered template

- [ ] add a `sample-config` command that prints an example config
    - README should instruct users to `clerk sample-config > /path/to/config/file`
    - since our config files are hidden in appdirs, maybe we should have a `generate-config` command that writes it _for_ them?
- [ ] add Google Tasks API integration
    - add a config option/flag to seed new journals with Google Tasks
    - a config option to update Google Tasks whenever I save my journal
        - maybe config file hooks for `on_create`, `on_open`, `on_save` and `on_discard`?
- [ ] add an error log in the appdir
- [ ] publish package
    - create a `console_scripts` "alias" for `journal`
    - setup.cfg, pyproject.toml


### Hooks functionality
- [X] add hooks functionality to main function
- [X] update config to parse hook specifications from config files
- [X] figure out how hooks get installed
- [X] write a simple hook to append a timestamp
