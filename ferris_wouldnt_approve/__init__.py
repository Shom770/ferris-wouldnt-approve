import sys

from importlib import invalidate_caches
from importlib.abc import Loader
from importlib.machinery import FileFinder


def _overload_format(self, format_spec):
    """
    Allows Rust-style attribute access for modules.

    >>> print(f"{random::randint(1, 5)}")
    4
    """
    if not format_spec.startswith(":"):
        raise SyntaxError(f"Missing target name for module {type(self).__name__!r}")

    format_spec = f":{format_spec}"

    targets = [target for target in format_spec.split("::") if target]

    result = self

    for target in targets:
        if "(" not in target:
            result = getattr(result, target)
        else:
            arguments = target.split("(")[-1].removesuffix(")")

            if arguments:
                result = getattr(result, target.split("(")[0])(eval(arguments))
            else:
                result = getattr(result, target.split("(")[0])()

    return str(result)


class AddFormatSpecsLoader(Loader):
    """Loader to add __format__ on import for not so Pythonic imports."""
    def __init__(self, *_):
        pass

    def create_module(self, spec):
        self.origin = spec.origin
        return

    def exec_module(self, module):
        with open(self.origin) as file:
            source = file.read()

        setattr(module, "__format__", _overload_format)

        exec(source, vars(module))


loader_details = AddFormatSpecsLoader, [".py"]

# Add path hook in front of others
sys.path_hooks.insert(0, FileFinder.path_hook(loader_details))
sys.path_importer_cache.clear()
invalidate_caches()
