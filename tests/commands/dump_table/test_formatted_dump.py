import sys
from collections import OrderedDict
from unittest.mock import patch

import pytest
from bide.commands.dump_table import dump_table
from bide.formatter import Formatter

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Does not work on Windows"
)


@pytest.fixture
def mock_formatter():
    with patch.object(Formatter, "__call__") as mock:
        yield mock


@pytest.mark.parametrize(
    "args, expected",
    [
        ({"symbol": "test_int", "format": ["I"]}, [(0, {"unnamed0": 0xDEADCAFE})]),
        (
            {"symbol": "test_array", "format": ["L", "8s", "L", "string"]},
            [
                (
                    0,
                    {
                        "unnamed0": 0,
                        "unnamed1": "value20",
                        "unnamed2": 30,
                        "unnamed3": "value40",
                    },
                ),
                (
                    1,
                    {
                        "unnamed0": 1,
                        "unnamed1": "value21",
                        "unnamed2": 31,
                        "unnamed3": "value41",
                    },
                ),
                (
                    2,
                    {
                        "unnamed0": 2,
                        "unnamed1": "value22",
                        "unnamed2": 32,
                        "unnamed3": "value42",
                    },
                ),
            ],
        ),
        (
            {"symbol": "test_array_symbols", "format": ["L", "symbol", "L", "symbol"]},
            [
                (
                    0,
                    {"unnamed0": 0, "unnamed1": "0", "unnamed2": 30, "unnamed3": "f1"},
                ),
                (
                    1,
                    {"unnamed0": 1, "unnamed1": "f2", "unnamed2": 31, "unnamed3": "f3"},
                ),
                (
                    2,
                    {"unnamed0": 2, "unnamed1": "f1", "unnamed2": 32, "unnamed3": "f2"},
                ),
            ],
        ),
    ],
    indirect=["args"],
)
def test_formatted_dump(test_executable, args, expected, mock_formatter):
    """Formatted dump should return expected output."""
    dump_table(args)
    mock_formatter.assert_called_once_with("dump_table", OrderedDict(expected))


@pytest.mark.parametrize(
    "args",
    [{"symbol": "test_array", "format": ["col:L", "col2:L", "col3:L", "col:L"]}],
    indirect=["args"],
)
def test_duplicate_column(test_executable, args):
    """Formatted dump should return ValueError for a duplicate column name."""
    with pytest.raises(ValueError) as exc_info:
        dump_table(args)
    assert "Duplicate column name" in str(exc_info)


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(
            {"symbol": "int_array", "format": ["I"], "topn": 1},
            [(0, {"unnamed0": 10})],
            id="topn=1",
        ),
        pytest.param(
            {"symbol": "int_array", "format": ["I"], "topn": 2},
            [(0, {"unnamed0": 10}), (1, {"unnamed0": 20})],
            id="topn=2",
        ),
    ],
    indirect=["args"],
)
def test_topn(test_executable, args, expected, mock_formatter):
    """topn parameter species how many rows should be returned."""
    dump_table(args)
    mock_formatter.assert_called_once_with("dump_table", OrderedDict(expected))


@pytest.mark.parametrize(
    "args, expected",
    [
        pytest.param(
            {"symbol": "test_int", "format": ["2H"]},
            [(0, {"unnamed0": 0xCAFE, "unnamed1": 0xDEAD})],
            id="simple_repeat",
        ),
    ],
    indirect=["args"],
)
def test_repeat(test_executable, args, expected, mock_formatter):
    """It should be possible to use a number with non-s format to specify multiple columns, e.g. 2L."""
    dump_table(args)
    mock_formatter.assert_called_once_with("dump_table", OrderedDict(expected))
