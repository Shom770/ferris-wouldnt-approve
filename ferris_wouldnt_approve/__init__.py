from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec

import sys


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


sys.path.insert(0, "")


class MyFinder(MetaPathFinder):
    def find_spec(self, name, *args):
        finder = [*filter(lambda i: "PathFinder" in str(i), sys.meta_path)][0]
        return ModuleSpec(name, ModuleLoader(name, finder.find_spec(name).origin))


class ModuleLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(self.filename) as file:
            data = file.read()

        module.__format__ = _overload_format

        exec(data, vars(module))


loader_details = ModuleLoader, [".py"]
