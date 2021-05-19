import os
from _pytest.fixtures import SubRequest
import pytest
import shutil
import tempfile

from jeroenbos.partest.utils import append_to_file

# all these fixtures are made available to scope tests/** by the import statement in tests/conftest.py


@pytest.fixture
def temp_test_directory(request: SubRequest):
    dir = tempfile.gettempdir()
    yield dir

    shutil.rmtree(dir)


@pytest.fixture
def temp_test_file():
    path = tempfile.mktemp("_test.py")
    append_to_file(
        path,
        """
import os
os.environ["METATESTING"] = "true"

import pytest

""",
    )
    yield path
    os.remove(path)