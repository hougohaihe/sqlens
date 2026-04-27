"""Markdown formatter for query execution plans."""

from sqlens.parsers.base import PlanNode


def _node_to_md(node: PlanNode, depth: int = 0) -> list[str]:
    """Recursively convert a PlanNode to Markdown lines."""
    indent = "  " * depth
    bullet = f"{indent}- "

    label_parts = [f"**{node.node_type}**"]
    if node.relation:
        label_parts.append(f"on `{node.relation}`")
    if node.cost is not None:
        label_parts.append(f"*(cost: {node.cost:.2f})*")
    if node.rows is not None:
        label_parts.append(f"*(rows: {node.rows})*")

    lines = [bullet + " ".join(label_parts)]

    for key, value in node.extra.items():
        lines.append(f"{indent}  - `{key}`: {value}")

    for child in node.children:
        lines.extend(_node_to_md(child, depth + 1))

    return lines


def format_plan(root: PlanNode) -> str:
    """Format a plan tree as a Markdown bullet list.

    Args:
        root: The root PlanNode of the execution plan.

    Returns:
        A Markdown-formatted string representation of the plan.
    """
    lines = _node_to_md(root, depth=0)
    return "\n".join(lines) + "\n"
