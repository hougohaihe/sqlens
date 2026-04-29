"""
Tests for sqlens/formatters/dot.py
"""
import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters import dot as dot_module
from sqlens.formatters.dot import format_plan


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def leaf_node() -> PlanNode:
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        estimated_cost=12.5,
        actual_rows=100,
        children=[],
    )


@pytest.fixture()
def nested_plan() -> PlanNode:
    left = PlanNode(node_type="Seq Scan", relation="orders", estimated_cost=8.0, actual_rows=50, children=[])
    right = PlanNode(node_type="Index Scan", relation="products", estimated_cost=4.0, actual_rows=20, children=[])
    return PlanNode(
        node_type="Hash Join",
        relation=None,
        estimated_cost=25.0,
        actual_rows=40,
        children=[left, right],
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_format_plan_returns_string(leaf_node):
    result = format_plan(leaf_node)
    assert isinstance(result, str)


def test_format_plan_starts_with_digraph(leaf_node):
    result = format_plan(leaf_node)
    assert result.startswith("digraph execution_plan {")


def test_format_plan_ends_with_closing_brace(leaf_node):
    result = format_plan(leaf_node)
    assert result.strip().endswith("}")


def test_format_plan_contains_node_type(leaf_node):
    result = format_plan(leaf_node)
    assert "Seq Scan" in result


def test_format_plan_contains_relation(leaf_node):
    result = format_plan(leaf_node)
    assert "users" in result


def test_format_plan_contains_cost(leaf_node):
    result = format_plan(leaf_node)
    assert "cost=12.50" in result


def test_format_plan_contains_rows(leaf_node):
    result = format_plan(leaf_node)
    assert "rows=100" in result


def test_format_plan_nested_has_edge(nested_plan):
    result = format_plan(nested_plan)
    # An edge is represented as "nodeX -> nodeY;"
    assert "->" in result


def test_format_plan_nested_contains_all_node_types(nested_plan):
    result = format_plan(nested_plan)
    assert "Hash Join" in result
    assert "Seq Scan" in result
    assert "Index Scan" in result


def test_format_plan_nested_node_count(nested_plan):
    """Three nodes => three node declarations."""
    result = format_plan(nested_plan)
    # Each node declaration ends with '];"
    assert result.count("];") == 3


def test_format_plan_no_relation_skips_on_clause():
    node = PlanNode(node_type="Aggregate", relation=None, estimated_cost=5.0, actual_rows=1, children=[])
    result = format_plan(node)
    assert "on " not in result
    assert "Aggregate" in result


def test_dot_module_registered():
    """Ensure the dot formatter is accessible via the formatter registry."""
    from sqlens.formatters import get_formatter
    mod = get_formatter("dot")
    assert mod is dot_module
