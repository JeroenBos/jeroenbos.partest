from io import StringIO
from _pytest.config import ExitCode

from jeroenbos.partest.pytest_with_reporting import run_pytest
from jeroenbos.partest.utils import to_string


class TestPytestWithReporting:
    def test_partest_on_empty_file(self, temp_test_file: str):
        exit_code = run_pytest([temp_test_file])
        assert exit_code == ExitCode.NO_TESTS_COLLECTED

    def test_output_when_testing_test_that_fails(self, failing_test_file: str):
        mock_sys_out = StringIO()

        reports = run_pytest([failing_test_file], mock_sys_out)
        output = to_string(mock_sys_out)

        assert isinstance(reports, list), f"Exit code: {reports}"
        assert len(reports) == 3  # setup, test and teardown events
        assert [report.when for report in reports] == ["setup", "call", "teardown"]
        assert [report.outcome for report in reports] == ["passed", "failed", "passed"]

        expected_log_fragments = [
            "Python 3.8.",
            "pytest-6.2.4, py-1.10.0, pluggy-0.13.1",
            "plugins: typeguard-2.12.0",
            "collected 1 item",
            """def test_that_fails():
>       raise ValueError("Intended to fail")
E       ValueError: Intended to fail""",
            "============================== 1 failed",
        ]
        for expected in expected_log_fragments:
            assert expected in output, f"{expected} not in {output}"
