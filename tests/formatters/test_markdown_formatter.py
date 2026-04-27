"""Tests for the Markdown plan formatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.markdown import format_plan


@pytest.fixture
def leaf_node():
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        cost=12.5,
        rows=100,
        children=[],
        extra={"Filter": "age > 18"},
    )


@pytest.fixture
def nested_plan():
    inner = PlanNode(
        node_type="Seq Scan",
        relation="orders",
        cost=8.0,
        rows=50,
        children=[],
        extra={},
    )
    return PlanNode(
        node_type="Hash Join",
        relation=None,
        cost=25.0,
        rows=200,
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
    assert "12.50" in result


def test_format_plan_contains_rows(leaf_node):
    result = format_plan(leaf_node)
    assert "100" in result


def test_format_plan_contains_extra_fields(leaf_node):
    result = format_plan(leaf_node)
    assert "Filter" in result
    assert "age > 18" in result


def test_format_plan_nested_contains_child(nested_plan):
    result = format_plan(nested_plan)
    assert "Hash Join" in result
    assert "Seq Scan" in result


def test_format_plan_nested_indents_child(nested_plan):
    result = format_plan(nested_plan)
    lines = result.splitlines()
    child_lines = [l for l in lines if "Seq Scan" in l]
    assert child_lines, "Expected a line containing 'Seq Scan'"
    assert child_lines[0].startswith("  "), "Child node should be indented"


def test_format_plan_no_relation_skips_on(nested_plan):
    result = format_plan(nested_plan)
    root_line = result.splitlines()[0]
    assert "on" not in root_line


def test_format_plan_ends_with_newline(leaf_node):
    result = format_plan(leaf_node)
    assert result.endswith("\n")
