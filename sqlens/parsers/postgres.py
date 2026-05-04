"""Parser for PostgreSQL EXPLAIN (FORMAT JSON) output."""

import json
from typing import Any

from sqlens.parsers.base import BasePlanParser, PlanNode

_SKIP_KEYS = {"Plans", "Node Type", "Total Cost", "Plan Rows", "Actual Rows", "Actual Total Time"}


class PostgresPlanParser(BasePlanParser):
    """Parses the JSON output produced by PostgreSQL's EXPLAIN (FORMAT JSON, ANALYZE)."""

    @property
    def dialect(self) -> str:
        return "postgres"

    def parse(self, raw_plan: Any) -> PlanNode:
        """Parse Postgres EXPLAIN JSON output.

        Args:
            raw_plan: Either a JSON string or the already-decoded Python object
                      returned by psycopg2 / asyncpg.

        Returns:
            Root PlanNode of the execution plan tree.

        Raises:
            ValueError: If the input cannot be parsed into a valid plan structure.
        """
        if isinstance(raw_plan, str):
            try:
                raw_plan = json.loads(raw_plan)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON input for Postgres plan: {exc}") from exc

        # psycopg2 returns a list with one element; asyncpg returns a list of dicts
        if isinstance(raw_plan, list):
            if not raw_plan:
                raise ValueError("Empty plan list received from Postgres EXPLAIN output.")
            raw_plan = raw_plan[0]

        if not isinstance(raw_plan, dict):
            raise ValueError(
                f"Expected a dict for Postgres plan, got {type(raw_plan).__name__!r}."
            )

        plan_dict = raw_plan.get("Plan", raw_plan)
        return self._parse_node(plan_dict)

    def _parse_node(self, node: dict[str, Any]) -> PlanNode:
        details = {k: v for k, v in node.items() if k not in _SKIP_KEYS}
        plan_node = PlanNode(
            node_type=node.get("Node Type", "Unknown"),
            cost=node.get("Total Cost"),
            rows=node.get("Plan Rows"),
            actual_rows=node.get("Actual Rows"),
            actual_time_ms=node.get("Actual Total Time"),
            details=details,
        )
        for child in node.get("Plans", []):
            plan_node.children.append(self._parse_node(child))
        return plan_node
