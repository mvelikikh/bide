import argparse
from unittest.mock import patch

import bide.cli as cli
import pytest


def test_exception():
    """Raised Exception should result in the exit code 255."""
    with patch.object(argparse, "ArgumentParser", autospec=True) as parser:
        parser.side_effect = Exception
        result = cli.main()
        assert result == 255
