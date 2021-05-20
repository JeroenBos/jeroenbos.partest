import os
from _pytest.fixtures import SubRequest
import shutil
import tempfile
from pytest import fixture

from jeroenbos.partest.utils import append_to_file

# all these fixtures are made available to scope tests/** by the import statement in tests/conftest.py


@fixture
def temp_test_directory(request: SubRequest):
    dir = tempfile.gettempdir()
    yield dir

    shutil.rmtree(dir)


@fixture
def temp_test_file():
    path = tempfile.mktemp("_test.py")
    append_to_file(
        path,
        """
import os
os.environ["METATESTING"] = "true"

import pytest

""",
    )
    yield path
    os.remove(path)


@fixture
def failing_test_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
def test_that_fails():
    raise ValueError("Intended to fail")

""",
    )
    return temp_test_file
