import logging
from unittest.mock import patch

import bide.cli as cli
import pytest


@patch(
    "sys.argv",
    ["program", "dump-table", "--ora-binary", "some_path", "--verbose", "symbol"],
)
def test_verbose(mock_command):
    """Verbose logging is used."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        cli.main()
        assert cli.LOGGER.level == logging.DEBUG


@patch(
    "sys.argv",
    ["program", "dump-table", "--ora-binary", "some_path", "--quiet", "symbol"],
)
def test_quiet(mock_command):
    """Quiet logging is used."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        cli.main()
        assert cli.LOGGER.level == logging.WARNING
