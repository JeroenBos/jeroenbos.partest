from dataclasses import dataclass
from _pytest.reports import TestReport
from typing import Literal

from tests.utils import pytest_ignore


When = Literal["setup", "call", "teardown"]
Outcome = Literal["passed", "failed", "skipped"]


@pytest_ignore
@dataclass
class TestEvent:
    when: When
    outcome: Outcome

    def __eq__(self, o: object) -> bool:
        if isinstance(o, TestReport):
            return self.when == o.when and self.outcome == o.outcome
        return super().__eq__(o)
