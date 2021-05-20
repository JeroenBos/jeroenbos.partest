import os
import shutil
import tempfile
from pytest import fixture

from jeroenbos.partest.utils import append_to_file

# all these fixtures are made available to scope tests/** by the import statement in tests/conftest.py


@fixture
def temp_test_file():
    path = tempfile.mktemp("_test.py")
    append_to_file(
        path,
        """# flake8: noqa
# type: ignore
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
    return append_successful_test_file(temp_test_file)


def append_successful_test_file(temp_test_file: str) -> str:
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
class TestSkippedTestWithFailingTearDown(TestCase):
    @pytest.mark.skip("Intended to be skipped")
    def test_that_is_skipped():
        raise ValueError("Intended to be skipped")

    def tearDown(self):
        raise ValueError("Teardown intended to fail")

""",
    )
    return temp_test_file


@fixture
def test_with_failing_setup_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
class TestWithFailingTearDown(TestCase):
    def test_after_failed_setup(self):
        raise ValueError("After setup intended to fail")

    def setUp(self):
        raise ValueError("Setup intended to fail")

""",
    )
    return temp_test_file


@fixture
def test_with_failing_teardown_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
class TestWithFailingTearDown(TestCase):
    def test_before_failing_teardown(self):
        pass

    def tearDown(self):
        raise ValueError("Teardown intended to fail")

""",
    )
    return temp_test_file


@fixture
def test_with_failing_setup_and_teardown_file(test_with_failing_setup_file: str) -> str:
    append_to_file(
        test_with_failing_setup_file,
        """
    def tearDown(self):
        raise ValueError("Teardown intended to fail")

""",
    )
    return test_with_failing_setup_file


@fixture
def test_that_fails_and_teardown_file(temp_test_file: str) -> str:
    append_to_file(
        temp_test_file,
        """
class TestThatFailsWithFailingTearDown(TestCase):
    def test_before_failing_teardown(self):
        raise ValueError("Test intended to fail")

    def tearDown(self):
        raise ValueError("Teardown intended to fail")

""",
    )
    return temp_test_file


@fixture
def temp_test_directory():
    dir = tempfile.mkdtemp()

    append_successful_test_file(os.path.join(dir, "test_file1.py"))
    append_successful_test_file(os.path.join(dir, "nested", "test_file2.py"))

    yield dir

    try:
        shutil.rmtree(dir)
    except PermissionError:
        pass
