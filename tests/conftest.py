# this file `conftest.py` gets called by pytest automatically, before anything else
import logging
import sys
from typeguard import importhook
from tests import SrcTypeguardFinder

logging.getLogger().setLevel("DEBUG")

# prevent all imports in tests/ from requiring the prefix "src."
sys.path.insert(1, "./src")

# apply runtime typechecking to "./src"
importhook.install_import_hook([], cls=SrcTypeguardFinder)
