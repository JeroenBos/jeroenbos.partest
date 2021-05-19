from importlib.machinery import ModuleSpec, SourceFileLoader
from typing import List, Optional

from typeguard.importhook import TypeguardFinder, TypeguardLoader


class SrcTypeguardFinder(TypeguardFinder):
    """
    Finds all modules imported from `./src`, to install Typeguards on them.
    This finetunes `./tests/conftest.py::sys.path.insert(1, "./src")`.
    """

    path_prefixes: List[str] = []

    @classmethod
    def applies(cls, path: Optional[str]) -> bool:
        result = path is not None and any(path.startswith(prefix) for prefix in cls.path_prefixes)
        return result

    def find_spec(self, fullname, path=None, target=None):
        result = super(SrcTypeguardFinder, self).find_spec(fullname, path, target)
        if result is not None:
            return result

        spec: Optional[ModuleSpec] = self._original_pathfinder.find_spec(fullname, path, target)
        if spec is None:
            return None

        if not isinstance(spec.loader, SourceFileLoader):
            # this restriction is imposed by the superclass; don't know why. Just imitating
            return None

        if any(self.applies(path) for path in [spec.origin] + (spec.submodule_search_locations or [])):
            spec.loader = TypeguardLoader(spec.loader.name, spec.loader.path)
            return spec

        return None
