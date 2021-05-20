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
        if super().__eq__(o):
            return True
        if isinstance(o, str):
            return o == str(self)
        return False

    def __str__(self) -> str:
        return self.getvalue()
