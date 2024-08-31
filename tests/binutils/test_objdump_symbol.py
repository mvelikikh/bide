import sys

import bide.binutils as binutils
import pytest

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Does not work on Windows"
)


def test_dump_existent_symbol(test_executable):
    """Correct dump should be returned for an existent symbol."""
    expected = bytearray(b"\xfe\xca\xad\xde")
    actual = binutils.objdump_symbol("test_int")
    assert expected == actual


def test_dump_non_existent_symbol(test_executable):
    """Error should be thrown for a non-existent symbol."""
    with pytest.raises(ValueError):
        binutils.objdump_symbol("no_such_symbol")
