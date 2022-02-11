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
