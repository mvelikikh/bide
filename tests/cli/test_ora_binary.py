import argparse
import os
from unittest.mock import patch

import bide.cli as cli
import pytest
from bide.config import settings


@patch("sys.argv", ["program", "dump-table", "--ora-binary", "some_path", "symbol"])
def test_ora_binary_provided_by_user_exists(mock_command):
    """User provided existing file and it is used."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        cli.main()
        assert settings.ora_binary == "some_path"


@patch("sys.argv", ["program", "dump-table", "--ora-binary", "no_such_file", "symbol"])
def test_ora_binary_provided_by_user_does_not_exist(capsys):
    """User provided non-existent file and error is thrown."""
    with pytest.raises(SystemExit) as exc_info:
        cli.main()
    err = capsys.readouterr().err.rstrip()
    assert isinstance(exc_info.value.__context__, argparse.ArgumentError)
    assert "does not exist" in err


@patch("sys.argv", ["program", "dump-table", "symbol"])
@patch.dict("os.environ", {}, clear=True)
def test_default_no_ora_home():
    """Default oracle binary is used if a user binary is not provided.
    Error is thrown because ORACLE_HOME is not set"""
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        cli.main()
    assert "ORACLE_HOME is not set" in str(exc_info.value)


@patch("sys.argv", ["program", "dump-table", "symbol"])
@patch.dict("os.environ", {"ORACLE_HOME": "some_path"}, clear=True)
def test_default_uses_ora_home_that_exists(mock_command):
    """Default oracle binary is used if a user binary is not provided.
    ORACLE_HOME is set and ORACLE_HOME/bin/oracle exists."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        cli.main()
        ora_binary_expected = os.path.join(os.environ["ORACLE_HOME"], "bin", "oracle")
        assert settings.ora_binary == ora_binary_expected


@patch("sys.argv", ["program", "dump-table", "symbol"])
@patch.dict("os.environ", {"ORACLE_HOME": "some_path"}, clear=True)
def test_default_uses_ora_home_that_does_not_exist():
    """Default oracle binary is used if a user binary is not provided.
    ORACLE_HOME is set and ORACLE_HOME/bin/oracle does not exist."""
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        with pytest.raises(argparse.ArgumentTypeError) as exc_info:
            cli.main()
        assert "Wrong ORACLE_HOME" in str(exc_info.value)
