"""Formatters package for sqlens."""

from sqlens.formatters import text, json as json_fmt

__all__ = ["text", "json_fmt"]


def get_formatter(fmt: str):
    """Return a formatter module by name.

    Supported values: ``'text'``, ``'json'``.

    Raises
    ------
    ValueError
        If *fmt* is not a recognised formatter name.
    """
    _registry = {
        "text": text,
        "json": json_fmt,
    }
    if fmt not in _registry:
        raise ValueError(
            f"Unknown formatter {fmt!r}. "
            f"Supported formatters: {sorted(_registry)}"
        )
    return _registry[fmt]
