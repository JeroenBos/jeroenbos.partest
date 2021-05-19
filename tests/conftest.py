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

# apply runtime typechecking to "./src"
SrcTypeguardFinder.path_prefixes.append(EXTRA_PATH)
importhook.install_import_hook([], cls=SrcTypeguardFinder)
