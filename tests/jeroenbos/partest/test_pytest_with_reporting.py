import os
from _pytest.config import ExitCode

from jeroenbos.partest.pytest_with_reporting import run_pytest
from jeroenbos.partest.typings import TestEvent
from jeroenbos.partest.utils import markup
from tests.jeroenbos.partest.test_string_io import TestStringIO


class TestPytestWithReporting:
    def test_partest_on_empty_file(self, temp_test_file: str):
        exit_code = run_pytest([temp_test_file])
        assert exit_code == ExitCode.NO_TESTS_COLLECTED

    def test_pytest_header_output(self, failing_test_file: str):
        # Arrange
        pytest_out = TestStringIO()

        # Act
        run_pytest([failing_test_file], pytest_out)

        # Assert
        pytest_output = pytest_out.getvalue()
        expected_log_fragments = [
            "============================= test session starts =============================",
            "Python 3.8.",
            "pytest-6.2.4",
            "py-1.10.0",
            "pluggy-0.13.1",
            "plugins: typeguard-2.12.0",
        ]

        for expected in expected_log_fragments:
            assert expected in pytest_output, f"{expected} not in {pytest_output}"

    def test_output_when_testing_test_that_fails(self, failing_test_file: str):
        # Arrange
        pytest_output = TestStringIO()
        sys_output = TestStringIO()

        # Act
        reports = run_pytest([failing_test_file], pytest_output, sys_output)

        # Assert
        # Check reports
        assert isinstance(reports, list), f"Exit code: {reports}"
        assert reports == [TestEvent("setup", "passed"), TestEvent("call", "failed"), TestEvent("teardown", "passed")]

        # Check output
        assert sys_output == markup("F", "red")

        # Check pytest output
        assert "collected 1 item" in pytest_output
        assert "============================== 1 failed" in pytest_output
        assert (
            """def test_that_fails():
>       raise ValueError("Intended to fail")
E       ValueError: Intended to fail"""
            in pytest_output
        )

    def test_output_when_testing_skipped_test(self, skipped_test_file: str):
        # Arrange
        pytest_output = TestStringIO()
        sys_output = TestStringIO()

        # Act
        reports = run_pytest([skipped_test_file], pytest_output, sys_output)

        # Assert
        # Check reports
        assert isinstance(reports, list), f"Exit code: {reports}"
        assert reports == [TestEvent("setup", "skipped"), TestEvent("teardown", "passed")]

        # Check output
        assert sys_output == markup("s", "yellow")

        # Check pytest output
        assert "collected 1 item" in pytest_output

    def test_output_when_testing_skipped_test_with_failing_teardown(self, skipped_test_with_failing_teardown_file: str):
        # Arrange
        pytest_output = TestStringIO()
        sys_output = TestStringIO()

        # Act
        reports = run_pytest([skipped_test_with_failing_teardown_file], pytest_output, sys_output)

        # Assert
        # Check reports
        assert reports == [TestEvent("setup", "skipped"), TestEvent("teardown", "passed")]
        #                                                                        ^^^^^^
        # The failing teardown method is skipped, and the actual pytest teardown passes

        # Check output
        assert sys_output == markup("s", "yellow")

    def test_output_with_successful_test(self, successful_test_file: str):
        # Arrange
        pytest_output = TestStringIO()
        sys_output = TestStringIO()

        # Act
        reports = run_pytest([successful_test_file], pytest_output, sys_output)

        # Assert
        # Check reports
        assert reports == [TestEvent("setup", "passed"), TestEvent("call", "passed"), TestEvent("teardown", "passed")]

        # Check output
        assert sys_output == markup(".", "green")

        assert "collected 1 item" in pytest_output
        assert "============================== 1 passed" in pytest_output

    def test_directory_structure(self, temp_test_directory: str):
        # Arrange
        pytest_output = TestStringIO()
        sys_output = TestStringIO()

        # Act
        reports = run_pytest([temp_test_directory], pytest_output, sys_output)

        # Assert
        # Check reports
        print(pytest_output)
        assert reports == 2 * [
            TestEvent("setup", "passed"),
            TestEvent("call", "passed"),
            TestEvent("teardown", "passed"),
        ]

        # Check output
        assert sys_output == 2 * markup(".", "green")

        assert os.path.join("nested", "test_file2.py") in pytest_output
        assert "collected 2 items" in pytest_output
        assert "============================== 2 passed" in pytest_output
