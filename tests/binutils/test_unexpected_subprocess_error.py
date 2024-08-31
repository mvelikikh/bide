import subprocess
from unittest.mock import patch

import bide.binutils as binutils
import pytest


def test_unexpected_subprocess_error(test_executable):
    """Correct string should be returned."""
    with patch.object(subprocess, "getstatusoutput", autospec=True) as mock_subprocess:
        mock_subprocess.return_value = (1, "test error")
        with pytest.raises(RuntimeError):
            binutils.objdump_symbol("test_string")
