from __future__ import annotations

import re
from typing import Any

from sqlens.parsers.base import BasePlanParser, PlanNode


class SQLitePlanParser(BasePlanParser):
    """Parser for SQLite EXPLAIN QUERY PLAN output."""

    dialect = "sqlite"

    # SQLite EXPLAIN QUERY PLAN rows look like:
    # id  parent  notused  detail
    _ROW_RE = re.compile(
        r"^(?P<id>\d+)\s+(?P<parent>\d+)\s+(?P<notused>\d+)\s+(?P<detail>.+)$"
    )

    def parse(self, raw: Any) -> PlanNode:
        """Parse SQLite EXPLAIN QUERY PLAN output.

        Accepts either a list of row tuples/dicts or a multi-line string
        produced by running EXPLAIN QUERY PLAN in the sqlite3 CLI.
        """
        rows = self._normalise_input(raw)
        if not rows:
            raise ValueError("Empty plan input")

        nodes: dict[int, PlanNode] = {}
        order: list[int] = []

        for row in rows:
            node_id = int(row["id"])
            parent_id = int(row["parent"])
            detail = row["detail"].strip()

            node = PlanNode(
                node_type=self._extract_type(detail),
                detail=detail,
                children=[],
                extra={"id": node_id, "parent": parent_id},
            )
            nodes[node_id] = node
            order.append((node_id, parent_id))

        # Build tree
        root: PlanNode | None = None
        for node_id, parent_id in order:
            if parent_id == 0:
                root = nodes[node_id]
            else:
                parent = nodes.get(parent_id)
                if parent is not None:
                    parent.children.append(nodes[node_id])

        if root is None:
            raise ValueError("Could not determine root node from plan")
        return root

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _normalise_input(self, raw: Any) -> list[dict]:
        """Accept list-of-tuples, list-of-dicts, or a plain string."""
        if isinstance(raw, str):
            rows = []
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                m = self._ROW_RE.match(line)
                if m:
                    rows.append(m.groupdict())
            return rows

        result = []
        for row in raw:
            if isinstance(row, dict):
                result.append({k.lower(): str(v) for k, v in row.items()})
            else:
                # assume iterable of (id, parent, notused, detail)
                result.append(
                    {"id": str(row[0]), "parent": str(row[1]),
                     "notused": str(row[2]), "detail": str(row[3])}
                )
        return result

    @staticmethod
    def _extract_type(detail: str) -> str:
        """Derive a short node type label from the detail string."""
        upper = detail.upper()
        for keyword in (
            "SCAN", "SEARCH", "USE TEMP B-TREE", "USE TEMP",
            "COMPOUND SUBQUERIES", "SUBQUERY", "CORRELATED SCALAR",
        ):
            if keyword in upper:
                return keyword.title().replace(" ", "")
        return "Step"
