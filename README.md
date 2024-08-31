![Python](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.11-blue) ![GitHub actions](https://github.com/mvelikikh/bide/actions/workflows/test.yml/badge.svg)

# BIDE

**bide** stands for binary data extractor. It is a command line utility to extract and parse data from the Oracle binary.

# Prerequisites
- Linux only
- Python 3
- Requires the binutils package since it calls nm, objdump, readelf under the hood
- Tested with Oracle Database versions: 19c (19.22), 23c (23.3)

# Installation

Download the directory [bide](.) and run from it:

```bash
pip install .
```

# Usage

## dump-table

```bash
usage: bide dump-table [-h] [-b ORA_BINARY] [-v | -q] [-o {table,json,html}] [-w WIDTH | --format FORMAT [FORMAT ...]] [--topn TOPN] [--offset OFFSET] [--roffset ROFFSET]
                       [--max-string-length MAX_STRING_LENGTH] [--no-decode-bytes-as-string]
                       symbol

Dump a symbol as a table using a provided format or display its bytes as hex.

positional arguments:
  symbol                A symbol to dump.

optional arguments:
  -h, --help            show this help message and exit
  -b ORA_BINARY, --ora-binary ORA_BINARY
                        Specify the path to Oracle binary. The program will look for $ORACLE_HOME/bin/oracle if no binary is specified
  -v, --verbose         Enable verbose output
  -q, --quiet           Enable silent mode (only show warnings and errors)
  -o {table,json,html}, --output {table,json,html}
                        The formatting style for command output
  -w WIDTH, --width WIDTH
                        Display this number of bytes per line. It is used with unformatted dump.
  --format FORMAT [FORMAT ...]
                        Format output based on the format. The format value is defined as: [column:]{format}. Where <column> is a user provided column header. <format> is one of Python format characters:
                        https://docs.python.org/3/library/struct.html#format-characters . When <column> is not provided it is named as "unnamed<index>" where <index> is a column position. In addition to
                        Python formats, two additional formats are defined: <symbol> - to dereference a symbol via the symbol table. <string> - a zero-byte terminated string. Numeric format modifiers, e.g.
                        3L, are supported.
  --topn TOPN           Stop processing after retrieving topn rows.
  --offset OFFSET       Dump starting with this offset.
  --roffset ROFFSET     Exclude this number of bytes at the end.
  --max-string-length MAX_STRING_LENGTH
                        Maximum string length for zero-byte terminated strings.
  --no-decode-bytes-as-string
                        Set to disable decoding bytes as null terminated strings.
```

# Examples

## Unformatted dump

```bash
$ bide dump-table skdxta
4c248414 00000000 04000000 00000000
80314a10 00000000 74107715 00000000
00000000 00000000 00000000 00000000
b4107715 00000000 08000000 00000000
40324a10 00000000 c0107715 00000000
00000000 00000000 00000000 00000000
```

## Unformatted dump showing 48 bytes per line

```bash
$ bide dump-table skdxta -w 48
4c248414 00000000 04000000 00000000 80314a10 00000000 74107715 00000000 00000000 00000000 00000000 00000000
b4107715 00000000 08000000 00000000 40324a10 00000000 c0107715 00000000 00000000 00000000 00000000 00000000
```

## Formatted dump

```bash
$ bide dump-table skdxta --format 4L H H I L
+-----------+----------+-----------+-----------+----------+----------+----------+----------+
|  unnamed0 | unnamed1 |  unnamed2 |  unnamed3 | unnamed4 | unnamed5 | unnamed6 | unnamed7 |
+-----------+----------+-----------+-----------+----------+----------+----------+----------+
| 344204364 |        4 | 273297792 | 360124532 |        0 |        0 |        0 |        0 |
| 360124596 |        8 | 273297984 | 360124608 |        0 |        0 |        0 |        0 |
+-----------+----------+-----------+-----------+----------+----------+----------+----------+
```

## Formatted dump with custom column headers to demonstrate that `%_ptr` columns (pointers) are automatically converted to hex by the formatter

```bash
$ bide dump-table skdxta --format a_ptr:L L b_ptr:L c_ptr:L H H I L
+------------+----------+------------+------------+----------+----------+----------+----------+
|      a_ptr | unnamed1 |      b_ptr |      c_ptr | unnamed4 | unnamed5 | unnamed6 | unnamed7 |
+------------+----------+------------+------------+----------+----------+----------+----------+
| 0x1484244c |        4 | 0x104a3180 | 0x15771074 |        0 |        0 |        0 |        0 |
| 0x157710b4 |        8 | 0x104a3240 | 0x157710c0 |        0 |        0 |        0 |        0 |
+------------+----------+------------+------------+----------+----------+----------+----------+
```

## Formatted dump dereferencing strings and symbols with custom column headers

```bash
$ bide dump-table skdxta --format cmd:string len:L func:symbol help:string H flags:H I check_func:symbol
+----------+-----+----------+--------------------------------------------------------------+----------+-------+----------+------------+
| cmd      | len | func     | help                                                         | unnamed4 | flags | unnamed6 | check_func |
+----------+-----+----------+--------------------------------------------------------------+----------+-------+----------+------------+
| CORE     |   4 | skdxcore |                           Dump core without crashing process |        0 |     0 |        0 | 0          |
| PROCSTAT |   8 | skdxprst |                           Dump process statistics            |        0 |     0 |        0 | 0          |
+----------+-----+----------+--------------------------------------------------------------+----------+-------+----------+------------+
```

## Formatted dump showing first 5 rows only

```bash
$ bide dump-table kqfsiz --format com:9s typ:9s dsc:38s siz:L --topn 5
+-----+-------+---------------+-----+
| com | typ   | dsc           | siz |
+-----+-------+---------------+-----+
| S   | EWORD | EITHER WORD   |   4 |
| S   | EB1   | EITHER BYTE 1 |   1 |
| S   | EB2   | EITHER BYTE 2 |   2 |
| S   | EB4   | EITHER BYTE 4 |   4 |
| S   | UWORD | UNSIGNED WORD |   4 |
+-----+-------+---------------+-----+
```
