"""Dump a symbol as a table using a provided format or display its bytes as hex."""

import argparse
import logging
import re
import struct
from collections import OrderedDict

import bide.binutils as binutils
from bide.formatter import get_formatter

LOGGER = logging.getLogger(__name__)

FORMAT_RE = re.compile(
    r"^((?P<column_name>[^:]+):)?(?P<repeat_count>\d+)?(?P<format>symbol|string|[xcbB?hHiIlLqQnNefdspP])$"
)


def _dump_table_args(p):
    """Return argparse command arguments."""

    def format_item(value):
        if not FORMAT_RE.match(value):
            raise argparse.ArgumentTypeError("Invalid format: %r" % (value))
        return value

    p.add_argument("symbol", help="A symbol to dump.")
    group = p.add_mutually_exclusive_group()
    group.add_argument(
        "-w",
        "--width",
        type=int,
        help="Display this number of bytes per line. It is used with unformatted dump.",
    )
    group.add_argument(
        "--format",
        type=format_item,
        nargs="+",
        help=(
            "Format output based on the format. "
            "The format value is defined as: [column:]{format}. "
            "Where <column> is a user provided column header.  "
            "<format> is one of Python format characters: "
            "https://docs.python.org/3/library/struct.html#format-characters . "
            "When <column> is not provided it is named as "
            '"unnamed<index>" where <index> is a column position. '
            "In addition to Python formats, two additional formats are defined: "
            "<symbol> - to dereference a symbol via the symbol table. "
            "<string> - a zero-byte terminated string. "
            "Numeric format modifiers, e.g. 3L, are supported."
        ),
    )
    p.add_argument(
        "--topn", type=int, help="Stop processing after retrieving topn rows."
    )
    p.add_argument("--offset", type=int, help="Dump starting with this offset.")
    p.add_argument(
        "--roffset", type=int, help="Exclude this number of bytes at the end."
    )
    p.add_argument(
        "--max-string-length",
        type=int,
        default=64,
        help="Maximum string length for zero-byte terminated strings.",
    )
    p.add_argument(
        "--no-decode-bytes-as-string",
        action="store_false",
        dest="decode_bytes_as_string",
        default=True,
        help="Set to disable decoding bytes as null terminated strings.",
    )


def _unformatted_dump(dump, args):
    text = dump.hex()
    width = args.width if args.width else 16
    hex_width = width * 2
    output = []
    for i in range(0, len(text), hex_width):
        output.append(" ".join([text[j : j + 8] for j in range(i, i + hex_width, 8)]))
        if args.topn and len(output) == args.topn:
            break
    print("\n".join(output))


def _extended_format_to_native(format_):
    extended_format_map = {"string": "P", "symbol": "P"}
    return extended_format_map.get(format_, format_)


def _construct_cols_from_format(formats):
    def add_col(name, format_):
        nonlocal col_index
        if name in col_names_seen:
            raise ValueError("Duplicate column name: %s" % (name))
        cols[col_index] = {"name": name, "format": format_}
        col_index += 1
        col_names_seen.add(name)

    unnamed_col_fmt = "unnamed%d"
    cols = {}
    col_index = 0
    col_names_seen = set()
    for format_ in formats:
        match_ = FORMAT_RE.match(format_)
        LOGGER.debug(match_)
        col_name = match_.group("column_name")
        fmt = match_.group("format")
        repeat_count = match_.group("repeat_count")
        # "s" with the repeat count should be interpreted as one column:
        # https://docs.python.org/3/library/struct.html#format-characters
        if repeat_count and fmt != "s":
            for i in range(int(repeat_count)):
                name = col_name + str(i) if col_name else unnamed_col_fmt % col_index
                add_col(name, fmt)
        else:
            name = col_name if col_name else unnamed_col_fmt % col_index
            fmt = repeat_count + fmt if repeat_count else fmt
            add_col(name, fmt)
    return cols


def _parse_dump(dump, cols, args):
    formats = (col["format"] for col in cols.values())
    native_format = "".join(_extended_format_to_native(fmt) for fmt in formats)
    parsed_dump = OrderedDict()
    symbol_addrs = []
    string_addrs = []
    for i, row in enumerate(struct.iter_unpack(native_format, dump)):
        LOGGER.debug("%5d %r", i, row)
        parsed_row = {}
        for j, col in enumerate(row):
            col_desc = cols[j]
            if col_desc["format"] == "string" and col > 0:
                string_addrs.append((i, col_desc["name"], col))
            elif col_desc["format"] == "symbol" and col > 0:
                symbol_addrs.append((i, col_desc["name"], col))
            # cast 0 to str to be in line with other values in the same column
            # formatter does alignment based on the column type
            elif col_desc["format"] in ("string", "symbol") and col == 0:
                col = str(col)
            elif isinstance(col, bytes) and args.decode_bytes_as_string:
                col = col.decode().strip("\x00")
            parsed_row[col_desc["name"]] = col
        parsed_dump[i] = parsed_row
        if args.topn and len(parsed_dump) == args.topn:
            break
    if symbol_addrs:
        symbols = binutils.get_symbols([addr for _, _, addr in symbol_addrs])
        for i, col, addr in symbol_addrs:
            parsed_dump[i][col] = symbols[addr]
    for i, col, addr in string_addrs:
        parsed_dump[i][col] = binutils.get_str_from_addr(addr, args.max_string_length)
    LOGGER.debug(parsed_dump)
    return parsed_dump


def _formatted_dump(dump, args):
    cols = _construct_cols_from_format(args.format)
    parsed_dump = _parse_dump(dump, cols, args)
    formatter = get_formatter(args.output)
    output = formatter("dump_table", parsed_dump)
    print(output)


def dump_table(args):
    """Command entry point."""
    LOGGER.debug(args)

    dump = binutils.objdump_symbol(args.symbol)
    if args.roffset:
        dump = dump[: -args.roffset]
    if args.offset:
        dump = dump[args.offset :]

    if args.format:
        _formatted_dump(dump, args)
    else:
        _unformatted_dump(dump, args)


def get_cmd_args():
    """Return metadata for argparse setup."""
    return ("dump-table", (dump_table, _dump_table_args, __doc__))
