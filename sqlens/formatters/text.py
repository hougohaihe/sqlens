"""Plain-text tree formatter for query plan nodes."""

from sqlens.parsers.base import PlanNode

_BRANCH = "├── "
_LAST   = "└── "
_PIPE   = "│   "
_BLANK  = "    "


def _node_label(node: PlanNode) -> str:
    """Build a concise label for a single plan node."""
    parts = [node.node_type]
    if node.relation:
        parts.append(f"on {node.relation}")
    extras = []
    if node.estimated_rows is not None:
        extras.append(f"rows={node.estimated_rows}")
    if node.actual_rows is not None:
        extras.append(f"actual={node.actual_rows}")
    if node.cost is not None:
        extras.append(f"cost={node.cost:.2f}")
    if extras:
        parts.append(f"({', '.join(extras)})")
    return " ".join(parts)


def _render_lines(node: PlanNode, prefix: str = "", is_last: bool = True) -> list[str]:
    connector = _LAST if is_last else _BRANCH
    line = f"{prefix}{connector}{_node_label(node)}" if prefix else _node_label(node)
    lines = [line]

    child_prefix = prefix + (_BLANK if is_last else _PIPE)
    children = node.children or []
    for i, child in enumerate(children):
        last_child = i == len(children) - 1
        lines.extend(_render_lines(child, child_prefix, last_child))
    return lines


def format_plan(root: PlanNode) -> str:
    """Return a human-readable tree string for *root*."""
    return "\n".join(_render_lines(root))
