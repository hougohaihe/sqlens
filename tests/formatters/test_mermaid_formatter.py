"""Tests for the Mermaid flowchart formatter."""

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.mermaid import format_plan


@pytest.fixture
def leaf_node() -> PlanNode:
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        estimated_cost=10.5,
        actual_rows=42,
        children=[],
        extra={},
    )


@pytest.fixture
def nested_plan() -> PlanNode:
    left = PlanNode(
        node_type="Seq Scan",
        relation="orders",
        estimated_cost=5.0,
        actual_rows=10,
        children=[],
        extra={},
    )
    right = PlanNode(
        node_type="Index Scan",
        relation="users",
        estimated_cost=3.0,
        actual_rows=5,
        children=[],
        extra={},
    )
    return PlanNode(
        node_type="Hash Join",
        relation=None,
        estimated_cost=20.0,
        actual_rows=15,
        children=[left, right],
        extra={},
    )


def test_format_plan_returns_string(leaf_node):
    result = format_plan(leaf_node)
    assert isinstance(result, str)


def test_format_plan_starts_with_graph_td(leaf_node):
    result = format_plan(leaf_node)
    assert result.startswith("graph TD")


def test_format_plan_contains_node_type(leaf_node):
    result = format_plan(leaf_node)
    assert "Seq Scan" in result


def test_format_plan_contains_relation(leaf_node):
    result = format_plan(leaf_node)
    assert "users" in result


def test_format_plan_contains_cost(leaf_node):
    result = format_plan(leaf_node)
    assert "cost=10.50" in result


def test_format_plan_contains_rows(leaf_node):
    result = format_plan(leaf_node)
    assert "rows=42" in result


def test_format_plan_nested_has_edges(nested_plan):
    result = format_plan(nested_plan)
    assert "-->" in result


def test_format_plan_nested_contains_all_types(nested_plan):
    result = format_plan(nested_plan)
    assert "Hash Join" in result
    assert "Seq Scan" in result
    assert "Index Scan" in result


def test_format_plan_nested_edge_count(nested_plan):
    result = format_plan(nested_plan)
    # Two children => two edges
    assert result.count("-->") == 2


def test_format_plan_no_relation_omits_on(leaf_node):
    leaf_node.relation = None
    result = format_plan(leaf_node)
    assert " on " not in result
