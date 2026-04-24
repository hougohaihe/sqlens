"""Base interface for query plan parsers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlanNode:
    """Represents a single node in a query execution plan tree."""

    node_type: str
    cost: Optional[float] = None
    rows: Optional[int] = None
    actual_rows: Optional[int] = None
    actual_time_ms: Optional[float] = None
    details: dict[str, Any] = field(default_factory=dict)
    children: list["PlanNode"] = field(default_factory=list)

    def is_leaf(self) -> bool:
        """Return True if this node has no children."""
        return len(self.children) == 0

    def total_nodes(self) -> int:
        """Recursively count all nodes in the subtree."""
        return 1 + sum(child.total_nodes() for child in self.children)

    def __repr__(self) -> str:
        cost_str = f", cost={self.cost}" if self.cost is not None else ""
        rows_str = f", rows={self.rows}" if self.rows is not None else ""
        return f"PlanNode(type={self.node_type!r}{cost_str}{rows_str})"


class BasePlanParser(ABC):
    """Abstract base class for database-specific plan parsers."""

    @abstractmethod
    def parse(self, raw_plan: Any) -> PlanNode:
        """Parse a raw query plan into a PlanNode tree.

        Args:
            raw_plan: The raw plan data from the database driver.

        Returns:
            The root PlanNode of the parsed plan tree.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def dialect(self) -> str:
        """Return the SQL dialect this parser handles (e.g. 'postgres', 'sqlite')."""
        raise NotImplementedError
