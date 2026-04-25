"""sqlens.parsers — plan parser registry."""
from __future__ import annotations

from typing import Type

from sqlens.parsers.base import BasePlanParser, PlanNode  # noqa: F401
from sqlens.parsers.postgres import PostgresPlanParser
from sqlens.parsers.sqlite import SQLitePlanParser

_REGISTRY: dict[str, Type[BasePlanParser]] = {
    PostgresPlanParser.dialect: PostgresPlanParser,
    SQLitePlanParser.dialect: SQLitePlanParser,
}


def get_parser(dialect: str) -> BasePlanParser:
    """Return an instantiated parser for *dialect*.

    Parameters
    ----------
    dialect:
        One of ``"postgres"`` or ``"sqlite"`` (case-insensitive).

    Raises
    ------
    ValueError
        If *dialect* is not recognised.
    """
    key = dialect.lower().strip()
    if key not in _REGISTRY:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Unknown dialect {dialect!r}. Supported dialects: {supported}"
        )
    return _REGISTRY[key]()


def supported_dialects() -> list[str]:
    """Return the list of supported dialect names."""
    return sorted(_REGISTRY.keys())
