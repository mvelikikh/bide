import pytest
from bide.formatter import TableFormatter


@pytest.fixture
def input_data():
    data = {
        0: {"col1": 0, "col2": "value20", "col3_ptr": 30, "col4": {"k": 40}},
        1: {"col1": 1, "col2": "value21", "col3_ptr": 31, "col4": {"k": 41}},
        2: {"col1": 2, "col2": "value22", "col3_ptr": 32, "col4": {"k": 42}},
    }
    yield data


def test_table_formatter(input_data):
    """Test that the correct tabular output is produced by the formatter."""
    formatter = TableFormatter()
    expected = """\
+------+---------+----------+-----------+
| col1 | col2    | col3_ptr | col4      |
+------+---------+----------+-----------+
|    0 | value20 |     0x1e | {'k': 40} |
|    1 | value21 |     0x1f | {'k': 41} |
|    2 | value22 |     0x20 | {'k': 42} |
+------+---------+----------+-----------+\
"""
    output = formatter("command", input_data).get_string()
    assert output == expected


def test_table_formatter_with_invalid_data_type():
    """Test that the formatter returns error on a non-dict input."""
    formatter = TableFormatter()
    with pytest.raises(ValueError):
        formatter("command", "not a dict")
