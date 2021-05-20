from io import StringIO
import os
import pytest
from typing import TextIO


def metatest(cls_or_f):
    """
    A decorator for test classes or test functions to indicate that it contains/is a test that
    is not intended to run as part of this repository's test suite, but will be used _by_ tests.
    """
    return pytest.mark.skipif(os.getenv("METATESTING", "false").lower() == "false")(cls_or_f)


def get_sink_io() -> TextIO:
    """
    Gets a TextIO that just sinks its input.
    """
    # TODO: Actually, I don't know of a type that sinks the input; will just put it in a string
    return StringIO()
