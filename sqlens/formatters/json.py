"""JSON formatter for query execution plan nodes."""

from __future__ import annotations

import json
from typing import Any, Dict

from sqlens.parsers.base import PlanNode


def _node_to_dict(node: PlanNode) -> Dict[str, Any]:
    """Recursively convert a PlanNode to a plain dictionary."""
    result: Dict[str, Any] = {
        "node_type": node.node_type,
    }

    if node.relation:
        result["relation"] = node.relation

    if node.estimated_cost is not None:
        result["estimated_cost"] = node.estimated_cost

    if node.actual_rows is not None:
        result["actual_rows"] = node.actual_rows

    if node.extra:
        result["extra"] = node.extra

    if node.children:
        result["children"] = [_node_to_dict(child) for child in node.children]

    return result


def format_plan(root: PlanNode, *, indent: int = 2) -> str:
    """Serialise the plan tree rooted at *root* to a JSON string.

    Parameters
    ----------
    root:
        The root ``PlanNode`` of the execution plan tree.
    indent:
        Number of spaces used for JSON indentation (default ``2``).

    Returns
    -------
    str
        A pretty-printed JSON representation of the plan.
    """
    return json.dumps(_node_to_dict(root), indent=indent)
