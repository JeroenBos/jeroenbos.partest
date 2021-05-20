from io import StringIO

from tests.utils import pytest_ignore


@pytest_ignore
class TestStringIO(StringIO):
    """
    Wraps io.StringIO with some helper methods.
    """

    def __contains__(self, value) -> bool:
        return value in str(self)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return o == str(self)
        return super().__eq__(o)

    def __str__(self) -> str:
        return self.getvalue()
