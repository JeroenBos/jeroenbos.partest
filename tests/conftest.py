# this file `conftest.py` gets called by pytest automatically, before anything else
import logging
import os
import sys
from typeguard import importhook
from tests import SrcTypeguardFinder

logging.getLogger().setLevel("DEBUG")

# prevent all imports in tests/ from requiring the prefix "src."
EXTRA_PATH = os.getcwd() + "/src"
sys.path.insert(1, EXTRA_PATH)

# apply runtime typechecking to "./src" and "./tests"
SrcTypeguardFinder.path_prefixes.extend([EXTRA_PATH, os.getcwd() + "/tests"])

importhook.install_import_hook([], cls=SrcTypeguardFinder)


# pull all fixtures into scope of the tests
from tests.jeroenbos.partest.fixtures.test_fixtures import *  # type: ignore  # noqa
