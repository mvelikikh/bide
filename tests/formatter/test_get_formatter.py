import pytest
from bide.formatter import (HTMLFormatter, JSONFormatter, TableFormatter,
                            get_formatter)


@pytest.mark.parametrize(
    "format_type, expected_formatter",
    [
        ("html", HTMLFormatter),
        ("table", TableFormatter),
        ("json", JSONFormatter),
    ],
)
def test_get_expected(format_type, expected_formatter):
    """Expected formatter is returned by get_formatter."""
    formatter = get_formatter(format_type)
    assert formatter.__class__.__name__ == expected_formatter.__name__


def test_get_unexpected():
    """Error is thrown when an unknown formatter is passed."""
    with pytest.raises(ValueError):
        get_formatter("unknown")
