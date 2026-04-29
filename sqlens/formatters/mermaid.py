"""Mermaid flowchart formatter for query execution plans."""

from sqlens.parsers.base import PlanNode


def _sanitise(text: str) -> str:
    """Escape characters that would break Mermaid syntax."""
    return text.replace('"', "'").replace("[", "(").replace("]", ")")


def _node_id(node: PlanNode, index: int) -> str:
    return f"N{index}"


def _collect_edges(
    node: PlanNode,
    counter: list,
    lines: list,
    parent_id: str | None = None,
) -> None:
    """Recursively collect node definitions and edges."""
    current_index = counter[0]
    current_id = _node_id(node, current_index)
    counter[0] += 1

    label_parts = [node.node_type]
    if node.relation:
        label_parts.append(f"on {node.relation}")
    if node.estimated_cost is not None:
        label_parts.append(f"cost={node.estimated_cost:.2f}")
    if node.actual_rows is not None:
        label_parts.append(f"rows={node.actual_rows}")

    label = _sanitise(" | ".join(label_parts))
    lines.append(f'    {current_id}["{label}"]')

    if parent_id is not None:
        lines.append(f"    {parent_id} --> {current_id}")

    for child in node.children:
        _collect_edges(child, counter, lines, current_id)


def format_plan(root: PlanNode) -> str:
    """Return a Mermaid flowchart string for *root*."""
    lines = ["graph TD"]
    counter = [0]
    _collect_edges(root, counter, lines)
    return "\n".join(lines) + "\n"
