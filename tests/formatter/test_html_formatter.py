import pytest
from bide.formatter import HTMLFormatter


@pytest.fixture
def input_data():
    data = {
        0: {"col1": 0, "col2": "value20", "col3_ptr": 30, "col4": {"k": 40}},
        1: {"col1": 1, "col2": "value21", "col3_ptr": 31, "col4": {"k": 41}},
        2: {"col1": 2, "col2": "value22", "col3_ptr": 32, "col4": {"k": 42}},
    }
    yield data


def test_html_formatter(input_data):
    """Test that the correct HTML output is produced by the formatter."""
    formatter = HTMLFormatter()
    expected = """\
<table>
    <thead>
        <tr>
            <th>col1</th>
            <th>col2</th>
            <th>col3_ptr</th>
            <th>col4</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>0</td>
            <td>value20</td>
            <td>0x1e</td>
            <td>{&#x27;k&#x27;: 40}</td>
        </tr>
        <tr>
            <td>1</td>
            <td>value21</td>
            <td>0x1f</td>
            <td>{&#x27;k&#x27;: 41}</td>
        </tr>
        <tr>
            <td>2</td>
            <td>value22</td>
            <td>0x20</td>
            <td>{&#x27;k&#x27;: 42}</td>
        </tr>
    </tbody>
</table>\
"""
    output = formatter("command", input_data)
    assert output == expected


def test_html_formatter_with_invalid_data_type():
    """Test that the formatter returns error on a non-dict input."""
    formatter = HTMLFormatter()
    with pytest.raises(ValueError):
        formatter("command", "not a dict")
