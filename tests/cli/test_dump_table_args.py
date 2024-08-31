import argparse
from unittest.mock import patch

import bide.cli as cli
import pytest


@patch(
    "sys.argv",
    ["program", "dump-table", "--format", "no_such_format", "symbol"],
)
def test_invalid_format(capsys):
    """Invalid format error is returned."""
    with pytest.raises(SystemExit) as exc_info:
        cli.main()
    assert isinstance(exc_info.value.__context__, argparse.ArgumentError)
    err = capsys.readouterr().err.rstrip()
    assert "Invalid format" in err


@patch(
    "sys.argv",
    [
        "program",
        "dump-table",
        "symbol",
        "--format",
        "symbol",
        "--ora-binary",
        "some_path",
    ],
)
def test_valid_format(mock_command):
    """Valid command should return no errors."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        assert cli.main() == 0
