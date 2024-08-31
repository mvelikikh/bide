import sys

import pytest
from bide.commands.dump_table import dump_table

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Does not work on Windows"
)


@pytest.mark.parametrize(
    "args, expected",
    [
        ({"symbol": "test_int"}, "fecaadde"),
        ({"symbol": "test_int", "offset": 1}, "caadde"),
        ({"symbol": "test_int", "roffset": 1}, "fecaad"),
        ({"symbol": "test_int", "offset": 1, "roffset": 1}, "caad"),
    ],
    indirect=["args"],
)
def test_unformatted_dump(test_executable, capsys, args, expected):
    """Unformatted dump should return expected output."""
    dump_table(args)
    out = capsys.readouterr().out.rstrip()
    assert out == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            {"symbol": "int_array", "topn": 1},
            "0a000000 14000000 1e000000 28000000",
        ),
        (
            {"symbol": "int_array", "topn": 2},
            (
                "0a000000 14000000 1e000000 28000000\n"
                "32000000 3c000000 46000000 50000000"
            ),
        ),
    ],
    indirect=["args"],
)
def test_topn(test_executable, capsys, args, expected):
    """Unformatted dump should return expected output."""
    dump_table(args)
    out = capsys.readouterr().out.rstrip()
    assert out == expected
