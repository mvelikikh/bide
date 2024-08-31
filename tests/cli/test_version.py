from unittest.mock import patch

import bide
import bide.cli as cli
import pytest


@patch("sys.argv", ["program", "--version"])
def test_version(capsys):
    """Correct version should be returned."""
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out.rstrip()
    assert out == bide._version.__version__
