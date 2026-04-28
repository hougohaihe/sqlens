"""Tests for the Markdown formatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.markdown import format_plan


@pytest.fixture
def leaf_node() -> PlanNode:
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        estimated_cost=10.5,
        estimated_rows=100,
        children=[],
        extra={"Filter": "age > 18"},
    )


@pytest.fixture
def nested_plan() -> PlanNode:
    inner = PlanNode(
        node_type="Index Scan",
        relation="orders",
        estimated_cost=5.0,
        estimated_rows=50,
        children=[],
        extra={},
    )
    return PlanNode(
        node_type="Hash Join",
        relation=None,
        estimated_cost=25.0,
        estimated_rows=200,
        children=[inner],
        extra={"Hash Cond": "(u.id = o.user_id)"},
    )


def test_format_plan_returns_string(leaf_node):
    result = format_plan(leaf_node)
    assert isinstance(result, str)


def test_format_plan_contains_node_type(leaf_node):
    result = format_plan(leaf_node)
    assert "Seq Scan" in result


def test_format_plan_contains_relation(leaf_node):
    result = format_plan(leaf_node)
    assert "users" in result


def test_format_plan_contains_cost(leaf_node):
    result = format_plan(leaf_node)
    assert "10.50" in result


def test_format_plan_contains_rows(leaf_node):
    result = format_plan(leaf_node)
    assert "100" in result


def test_format_plan_contains_extra(leaf_node):
    result = format_plan(leaf_node)
    assert "Filter" in result
    assert "age > 18" in result


def test_format_plan_nested_contains_parent(nested_plan):
    result = format_plan(nested_plan)
    assert "Hash Join" in result


def test_format_plan_nested_contains_child(nested_plan):
    result = format_plan(nested_plan)
    assert "Index Scan" in result


def test_format_plan_nested_child_indented(nested_plan):
    result = format_plan(nested_plan)
    lines = result.splitlines()
    child_lines = [l for l in lines if "Index Scan" in l]
    assert child_lines, "Expected a line containing 'Index Scan'"
    assert child_lines[0].startswith("  "), "Child node should be indented"


def test_format_plan_ends_with_newline(leaf_node):
    result = format_plan(leaf_node)
    assert result.endswith("\n")


def test_format_plan_uses_markdown_bold(leaf_node):
    result = format_plan(leaf_node)
    assert "**Seq Scan**" in result


def test_format_plan_no_relation_when_none(nested_plan):
    result = format_plan(nested_plan)
    lines = result.splitlines()
    parent_line = lines[0]
    assert "on `" not in parent_line
