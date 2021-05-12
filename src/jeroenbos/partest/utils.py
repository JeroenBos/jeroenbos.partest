from contextlib import contextmanager
from typing import ContextManager

from _pytest._io.terminalwriter import TerminalWriter


@contextmanager
def optional(condition: bool, context_manager: ContextManager):
    """
    Conditionally applies the specified context manager
    """
    if condition:
        with context_manager:
            yield
    else:
        yield


def markup(text: str, color: str = None) -> str:
    """
    Returns the specified string in the specified color for terminal output.
    """
    if color is None:
        return text

    if color not in TerminalWriter._esctable:
        raise ValueError(f"Unknown color: {color!r}")
    prefix = "\x1b[%sm" % TerminalWriter._esctable[color]
    postfix = "\x1b[0m"

    return f"{prefix}{text}{postfix}"
