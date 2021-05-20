import sys
from tests.utils import get_sink_io
from typing import List, Optional, TextIO, Union
from unittest.mock import patch

from _pytest._io.terminalwriter import TerminalWriter
from _pytest.config import Config, ExitCode, create_terminal_writer
from _pytest.main import Session
from _pytest.reports import CollectReport, TestReport
import pytest

from jeroenbos.partest.utils import markup, optional

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
) -> Union[ExitCode, List[Union[TestReport, CollectReport]]]:
    """
    Runs pytest.main with the specified args, and collects reports of all tests;
    or exit codes (per _pytest.config.ExitCode) in case it didn't get so far.
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
            self.reports: List[Union[TestReport, CollectReport]] = []

        def pytest_runtest_logreport(self, report):
            """
            :param report: Union[TestReport, CollectReport]
                           but you can't write the type definition,
                           because typeguard influences how pytest inspects it
            """
            super(_Session, self).pytest_runtest_logreport(report)
            self.reports.append(report)
            self.writer.write(get_summary_char(report), flush=True)

    return _Session


def get_summary_char(report: Union[TestReport, CollectReport]) -> str:
    if report.skipped:
        return markup("s", "yellow")
    elif report.failed:
        return markup("F", "red")
    else:
        return markup(".", "green")


def _create_terminal_writer_factory(output: Optional[TextIO]):
    """
    A factory method for creating a `create_terminal_writer` function.
    :param output: The receiver of all original pytest output.
    """

    def _create_terminal_writer(config: Config, _file: Optional[TextIO] = None) -> TerminalWriter:
        file = output if output is not None else get_sink_io()
        return create_terminal_writer(config, file)

    return _create_terminal_writer
