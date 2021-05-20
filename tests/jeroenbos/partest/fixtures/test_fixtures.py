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
import unittest
from unittest import TestCase

""",
    )
    yield path
    os.remove(path)


@fixture
def successful_test_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
def test_that_succeeds():
    pass

""",
    )
    return temp_test_file


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


@fixture
def skipped_test_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
@pytest.mark.skip("Intended to be skipped")
def test_that_is_skipped():
    raise ValueError("Intended to be skipped")

""",
    )
    return temp_test_file


@fixture
def skipped_test_with_failing_teardown_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
class TestWithFailingTearDown(TestCase):
    @pytest.mark.skip("Intended to be skipped")
    def test_that_is_skipped():
        raise ValueError("Intended to be skipped")

    def tearDown(self):
        raise ValueError("Teardown intended to fail")
""",
    )
    return temp_test_file
