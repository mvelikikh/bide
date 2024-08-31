import sys

import bide.binutils as binutils
import pytest

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Does not work on Windows"
)


def test_get_symbols(test_executable):
    """Correct address to symbol map should be returned for a list of addresses."""
    symbols = ["test_string", "test_int", "test_array"]
    addr_len_list = (binutils.get_addr_len(symbol) for symbol in symbols)
    addr_list = [addr for addr, _ in addr_len_list]
    symbol_map = dict(zip(addr_list, symbols))
    actual_symbols = binutils.get_symbols(addr_list)
    assert sorted(symbol_map) == sorted(actual_symbols)
