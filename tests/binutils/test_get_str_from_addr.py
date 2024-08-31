import struct
import sys

import bide.binutils as binutils
import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="Does not work on Windows")
def test_get_str_from_addr(test_executable):
    """Correct string should be returned."""
    expected = "test_string_value"
    dump = binutils.objdump_symbol("test_string")
    (addr,) = struct.unpack("Q", dump)
    actual = binutils.get_str_from_addr(addr, 64)
    assert expected == actual


@pytest.mark.skipif(sys.platform == "win32", reason="Does not work on Windows")
def test_get_str_from_addr_no_null(test_executable):
    """Reading a string from an address returns a value without NULL character.
    An error should be raised."""
    dump = binutils.objdump_symbol("test_string")
    (addr,) = struct.unpack("Q", dump)
    with pytest.raises(ValueError):
        binutils.get_str_from_addr(addr, 4)
