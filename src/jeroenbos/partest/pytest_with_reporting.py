from io import StringIO
import sys
from typing import Any, List, Optional, TextIO, Type, Union
from unittest.mock import patch

from _pytest._io.terminalwriter import TerminalWriter
from _pytest.config import Config, create_terminal_writer
from _pytest.main import Session
from _pytest.reports import CollectReport, TestReport
import pytest

from jeroenbos.partest.utils import markup, optional

OptionalTextIO = Union[Optional[TextIO], Any]  # Should be Optional[TextIO] but typeguard is buggy


def run_pytest(
    args: List[str],
    sys_out: OptionalTextIO = None,
) -> Union[int, List[Union[TestReport, CollectReport]]]:
    """
    Runs pytest.main with the specified args, and collects reports of all tests;
    or exit codes (per _pytest.config.ExitCode) in case it didn't get so far.
    """

    assert isinstance(args, list) and all(isinstance(arg, str) for arg in args)

    # create a new singleton _Session type
    __Session: Type[_Session] = object.__new__(_Session)
    c = _create_terminal_writer_factory(sys_out)
    with patch("_pytest.main.Session", __Session):
        with optional(
            sys_out is not sys.stdout,
            patch("_pytest.config.create_terminal_writer", c),
        ):
            exit_code = pytest.main(args)
            session = __Session.singleton
            if session is not None:
                return session.singleton.reports  # type: ignore
            else:
                return int(exit_code)


class _Session(Session):  # type: ignore
    """
    This class extends the Session in that it collects test reports,
    and writes single-character test summaries (.sF) to sysout.
    """

    singleton: "Optional[_Session]" = None

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.reports: List[Union[TestReport, CollectReport]] = []

    @classmethod
    def _set_singleton(cls, singleton: "_Session"):
        assert cls.singleton is None
        cls.singleton = singleton

    def pytest_runtest_logreport(self, report):
        """
        :param: Union[TestReport, CollectReport]
        """
        # but you can't write the type definition, because typeguard influences how pytest inspects it
        super(_Session, self).pytest_runtest_logreport(report)
        self.reports.append(report)
        sys.stdout.write(self.get_summary_char(report))
        sys.stdout.flush()

    def get_summary_char(self, report: Union[TestReport, CollectReport]) -> str:
        if report.skipped:
            return markup("s", "yellow")
        elif report.failed:
            return markup("F", "red")
        else:
            return markup(".", "green")


def _create_terminal_writer_factory(output: OptionalTextIO):
    """
    A factory method for creating a `create_terminal_writer` function.
    :param output: The receiver of all original pytest output.
    """

    def _create_terminal_writer(config: Config, file: Optional[TextIO] = None) -> TerminalWriter:
        dummyTextIO = output if output is not None else StringIO()
        return create_terminal_writer(config, dummyTextIO)

    return _create_terminal_writer
