from dataclasses import dataclass
from typing import Literal

from _pytest.reports import TestReport


When = Literal["setup", "call", "teardown"]
Outcome = Literal["passed", "failed", "skipped"]


@dataclass
class TestEvent:
    when: When
    outcome: Outcome

    def __eq__(self, o: object) -> bool:
        if isinstance(o, TestReport):
            return self.when == o.when and self.outcome == o.outcome
        return super().__eq__(o)
