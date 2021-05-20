from io import StringIO
from _pytest.config import ExitCode
from jeroenbos.partest.typings import TestEvent

from jeroenbos.partest.pytest_with_reporting import run_pytest
from jeroenbos.partest.utils import markup, to_string


class TestPytestWithReporting:
    def test_partest_on_empty_file(self, temp_test_file: str):
        exit_code = run_pytest([temp_test_file])
        assert exit_code == ExitCode.NO_TESTS_COLLECTED

    def test_pytest_header_output(self, failing_test_file: str):
        # Arrange
        pytest_out = StringIO()

        # Act
        run_pytest([failing_test_file], pytest_out)

        # Assert
        pytest_output = to_string(pytest_out)
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
        pytest_out = StringIO()
        sys_out = StringIO()

        # Act
        reports = run_pytest([failing_test_file], pytest_out, sys_out)

        # Assert
        # Check reports
        assert isinstance(reports, list), f"Exit code: {reports}"
        assert reports == [TestEvent("setup", "passed"), TestEvent("call", "failed"), TestEvent("teardown", "passed")]

        # Check output
        sys_output = to_string(sys_out)
        assert sys_output == markup("F", "red")

        # Check pytest output
        pytest_output = to_string(pytest_out)
        expected_log_fragments = [
            "collected 1 item",
            """def test_that_fails():
>       raise ValueError("Intended to fail")
E       ValueError: Intended to fail""",
            "============================== 1 failed",
        ]
        for expected in expected_log_fragments:
            assert expected in pytest_output, f"{expected} not in {pytest_output}"

    def test_output_when_testing_skipped_test(self, skipped_test_file: str):
        # Arrange
        pytest_out = StringIO()
        sys_out = StringIO()

        # Act
        reports = run_pytest([skipped_test_file], pytest_out, sys_out)

        # Assert
        # Check reports
        assert isinstance(reports, list), f"Exit code: {reports}"
        assert reports == [TestEvent("setup", "skipped"), TestEvent("teardown", "passed")]

        # Check output
        sys_output = to_string(sys_out)
        assert sys_output == markup("s", "yellow")

        # Check pytest output
        pytest_output = to_string(pytest_out)
        expected_log_fragments = [
            "collected 1 item",
        ]
        for expected in expected_log_fragments:
            assert expected in pytest_output, f"{expected} not in {pytest_output}"

    def test_output_when_testing_skipped_test_with_failing_teardown(self, skipped_test_with_failing_teardown_file: str):
        # Arrange
        pytest_out = StringIO()
        sys_out = StringIO()

        # Act
        reports = run_pytest([skipped_test_with_failing_teardown_file], pytest_out, sys_out)

        # Assert
        # Check reports
        assert reports == [TestEvent("setup", "skipped"), TestEvent("teardown", "passed")]
        #                                                                        ^^^^^^
        # The failing teardown method is skipped, and the actual pytest teardown passes

        # Check output
        sys_output = to_string(sys_out)
        assert sys_output == markup("s", "yellow")
