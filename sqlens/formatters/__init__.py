"""Formatter registry for sqlens."""

from types import ModuleType


def get_formatter(fmt: str) -> ModuleType:
    """Return the formatter module for *fmt*.

    Parameters
    ----------
    fmt:
        One of ``"text"``, ``"json"``, ``"html"``, ``"markdown"``, or
        ``"mermaid"``.

    Raises
    ------
    ValueError
        If *fmt* is not a supported formatter name.
    """
    if fmt == "text":
        from sqlens.formatters import text
        return text
    if fmt == "json":
        from sqlens.formatters import json
        return json
    if fmt == "html":
        from sqlens.formatters import html
        return html
    if fmt == "markdown":
        from sqlens.formatters import markdown
        return markdown
    if fmt == "mermaid":
        from sqlens.formatters import mermaid
        return mermaid

    supported = "text, json, html, markdown, mermaid"
    raise ValueError(
        f"Unknown formatter {fmt!r}. Supported formatters: {supported}"
    )
