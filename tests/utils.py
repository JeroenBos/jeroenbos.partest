import os
import pytest


def metatest(cls_or_f):
    """
    A decorator for test classes or test functions to indicate that it contains/is a test that
    is not intended to run as part of this repository's test suite, but will be used _by_ tests.
    """
    return pytest.mark.skipif(os.getenv("METATESTING", "false").lower() == "false")(cls_or_f)
