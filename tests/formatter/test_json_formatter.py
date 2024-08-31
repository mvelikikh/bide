import pytest
from bide.formatter import JSONFormatter


@pytest.fixture
def input_data():
    data = {
        0: {"col1": 0, "col2": "value20", "col3_ptr": 30, "col4": {"k": 40}},
        1: {"col1": 1, "col2": "value21", "col3_ptr": 31, "col4": {"k": 41}},
        2: {"col1": 2, "col2": "value22", "col3_ptr": 32, "col4": {"k": 42}},
    }
    yield data


def test_json_formatter(input_data):
    """Test that the correct JSON output is produced by the formatter."""
    formatter = JSONFormatter()
    expected = """\
{
  "0": {
    "col1": 0,
    "col2": "value20",
    "col3_ptr": 30,
    "col4": {
      "k": 40
    }
  },
  "1": {
    "col1": 1,
    "col2": "value21",
    "col3_ptr": 31,
    "col4": {
      "k": 41
    }
  },
  "2": {
    "col1": 2,
    "col2": "value22",
    "col3_ptr": 32,
    "col4": {
      "k": 42
    }
  }
}\
"""
    output = formatter("command", input_data)
    print(output)
    assert output == expected
