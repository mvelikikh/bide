from unittest.mock import patch

import bide.commands.dump_table as dump_table
import pytest


@pytest.fixture
def mock_command():
    """Mock a sample command called by the CLI module."""
    with patch.object(dump_table, "dump_table") as mock:
        yield mock
