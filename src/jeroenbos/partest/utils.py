from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import ContextManager, TextIO

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


def append_to_file(path: str, contents: str):
    """Appends the specified contents to the specified file"""

    # Create parent dir if not exists
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "a+") as f:
        f.write(contents)


def get_sink_io() -> TextIO:
    """
    Gets a TextIO that just sinks its input.
    """
    # TODO: Actually, I don't know of a type that sinks the input; will just put it in a string
    return StringIO()
