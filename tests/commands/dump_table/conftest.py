from argparse import Namespace

import pytest


@pytest.fixture
def args(request):
    """Create input arguments for dump_table."""
    args = Namespace(
        output="table",
        symbol=None,
        width=None,
        format=None,
        topn=None,
        offset=None,
        roffset=None,
        max_string_length=64,
        decode_bytes_as_string=True,
        command="dump-table",
    )
    for k, v in request.param.items():
        setattr(args, k, v)
    yield args
