"""
DOT (Graphviz) formatter for query execution plans.

Produces a DOT language string that can be rendered with Graphviz tools
(e.g. `dot -Tpng -o plan.png plan.dot`).
"""
from __future__ import annotations

from sqlens.parsers.base import PlanNode


def _sanitise(text: str) -> str:
    """Escape characters that are special inside DOT label strings."""
    return text.replace('"', "'").replace("<", "{").replace(">", "}")


def _node_id(node: PlanNode, counter: list[int]) -> str:
    """Return a unique node identifier and advance the counter."""
    node_id = f"node{counter[0]}"
    counter[0] += 1
    return node_id


def _node_label(node: PlanNode) -> str:
    """Build a human-readable label for a single plan node."""
    parts = [_sanitise(node.node_type)]
    if node.relation:
        parts.append(f"on {_sanitise(node.relation)}")
    if node.estimated_cost is not None:
        parts.append(f"cost={node.estimated_cost:.2f}")
    if node.actual_rows is not None:
        parts.append(f"rows={node.actual_rows}")
    return "\n".join(parts)


def _collect_statements(
    node: PlanNode,
    counter: list[int],
    statements: list[str],
) -> str:
    """Recursively emit node and edge declarations, return this node's id."""
    current_id = _node_id(node, counter)
    label = _node_label(node)
    statements.append(f'  {current_id} [label="{label}"];')

    for child in node.children:
        child_id = _collect_statements(child, counter, statements)
        statements.append(f"  {current_id} -> {child_id};")

    return current_id


def format_plan(root: PlanNode) -> str:
    """Return a DOT language representation of the execution plan tree."""
    counter = [0]
    statements: list[str] = []
    _collect_statements(root, counter, statements)

    body = "\n".join(statements)
    return (
        "digraph execution_plan {\n"
        '  node [shape=box fontname="Helvetica"];\n'
        f"{body}\n"
        "}"
    )
