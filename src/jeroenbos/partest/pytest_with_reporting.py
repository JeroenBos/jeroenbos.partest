import sys
from typing import List, Optional, TextIO, Union
from unittest.mock import patch

from _pytest._io.terminalwriter import TerminalWriter
from _pytest.config import Config, ExitCode, create_terminal_writer
from _pytest.main import Session
from _pytest.reports import TestReport
import pytest

from jeroenbos.partest.utils import markup, optional, get_sink_io

# About stdout:
# There are 3 sources of output:
# 1. from the system under test or the test itself
# 2. from the testing framework
# 3. from this wrapper around the testing framework
#
# pytest writes 1 and 2 to a TerminalWriter, which will write to the parameter `pytest_out`.
# The wrapper writes 3 to the specified parameter `out`


def run_pytest(
    args: List[str],
    pytest_out: Optional[TextIO] = None,
    out: Optional[TextIO] = None,
) -> Union[ExitCode, List[TestReport]]:
    """
    Runs pytest.main with the specified args, and collects reports of all tests;
    or exit codes (per _pytest.config.ExitCode) in case it didn't get so far.

    :param pytest_out: The output stream of pytest's output. Defaults to /dev/null.
    :param out: The output stream of this wrapper's output. Defaults to sys.std_out.
    """

    __Session = _create_Session(out)
    create_terminal_writer = _create_terminal_writer_factory(pytest_out)
    with patch("_pytest.main.Session", __Session):
        with optional(
            pytest_out is not sys.stdout,
            patch("_pytest.config.create_terminal_writer", create_terminal_writer),
        ):
            exit_code = pytest.main(args)
            if int(exit_code) in [ExitCode.OK, ExitCode.TESTS_FAILED] and __Session.instance:
                return __Session.instance.reports
            return exit_code if isinstance(exit_code, ExitCode) else ExitCode(exit_code)


def _create_Session(out: Optional[TextIO]):
    """:param out: will default to sys.out if None"""

    class _Session(Session):  # type: ignore
        """
        This class extends the Session in that it collects test reports,
        and writes single-character test summaries (.sF) to sysout.
        """

        instance: "Optional[_Session]" = None

        def __init__(self, config: Config) -> None:
            assert self.__class__.instance is None, "_Session singleton created multiple times"
            self.__class__.instance = self
            super().__init__(config)
            self.writer = TerminalWriter(out)
            self.reports: List[TestReport] = []

        def pytest_runtest_logreport(self, report):
            """
            :param report: Union[TestReport, CollectReport]
                           but you can't write the type definition,
                           because typeguard influences how pytest inspects it
            """
            assert isinstance(report, TestReport), "According to typing hints this could also be a CollectReport"
            super(_Session, self).pytest_runtest_logreport(report)
            self.reports.append(report)
            self.writer.write(get_summary_char(report), flush=True)

    return _Session


def get_summary_char(report: TestReport) -> str:
    if report.skipped:
        return markup("s", "yellow")
    elif report.failed:
        # A failing class setup or failing class teardown is considered an "error" -not a "failure"- by pytest,
        # in which case the failure or success of the test is logged separately.
        # The test nor the class teardown are run when the class setup failed.
        #
        # Also a failing test teardown after a failed test is considered an "error" by pytest.
        # (a failing test teardown after successful test is considered "failure", but is crucially in when=call)
        if report.when == "call":
            return markup("F", "red")
        else:
            return markup("E", "red")
    elif report.when == "call":
        return markup(".", "green")
    else:
        return ""


def _create_terminal_writer_factory(output: Optional[TextIO]):
    """
    A factory method for creating a `create_terminal_writer` function.
    :param output: The receiver of all original pytest output.
    """

    def _create_terminal_writer(config: Config, _file: Optional[TextIO] = None) -> TerminalWriter:
        file = output if output is not None else get_sink_io()
        return create_terminal_writer(config, file)

    return _create_terminal_writer
