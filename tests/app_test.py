from unittest.mock import patch

from src.app import main


@patch("subprocess.run")
def test_main(subprocess_run):
    main()
    breakpoint()
    assert subprocess_run.called_with()
