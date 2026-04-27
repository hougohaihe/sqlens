"""HTML formatter for query execution plans."""

from sqlens.parsers.base import PlanNode


def _node_to_html(node: PlanNode, depth: int = 0) -> str:
    """Recursively render a PlanNode as an HTML tree structure."""
    indent = "  " * depth

    parts = []
    if node.relation:
        parts.append(f"<span class='relation'>on {node.relation}</span>")
    if node.cost is not None:
        parts.append(f"<span class='cost'>cost={node.cost:.2f}</span>")
    if node.rows is not None:
        parts.append(f"<span class='rows'>rows={node.rows}</span>")

    meta = " ".join(parts)
    label = f"<span class='node-type'>{node.node_type}</span>"
    if meta:
        label = f"{label} {meta}"

    children_html = ""
    if node.children:
        child_items = "".join(
            f"\n{indent}    <li>{_node_to_html(child, depth + 2)}</li>"
            for child in node.children
        )
        children_html = f"\n{indent}  <ul>{child_items}\n{indent}  </ul>"

    return f"{label}{children_html}"


def format_plan(root: PlanNode) -> str:
    """Format a plan tree as a self-contained HTML snippet.

    Returns an HTML string with inline styles suitable for embedding
    in a report or notebook output.
    """
    style = (
        "<style>"
        ".sqlens-plan { font-family: monospace; font-size: 0.9em; }"
        ".sqlens-plan ul { list-style: none; padding-left: 1.5em; "
        "border-left: 1px dashed #ccc; margin: 2px 0; }"
        ".sqlens-plan .node-type { font-weight: bold; color: #2c5f8a; }"
        ".sqlens-plan .relation { color: #5a7a3a; }"
        ".sqlens-plan .cost { color: #8a5a2c; }"
        ".sqlens-plan .rows { color: #6a3a8a; }"
        "</style>"
    )
    body = f"<ul>\n  <li>{_node_to_html(root, depth=1)}</li>\n</ul>"
    return f"<div class='sqlens-plan'>\n{style}\n{body}\n</div>"
