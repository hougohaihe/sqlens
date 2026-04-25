"""Tests for the plain-text tree formatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.text import format_plan


@pytest.fixture
def leaf_node():
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        estimated_rows=1000,
        actual_rows=987,
        cost=42.5,
        children=[],
        raw={},
    )


@pytest.fixture
def nested_plan():
    inner = PlanNode(
        node_type="Seq Scan",
        relation="orders",
        estimated_rows=500,
        actual_rows=None,
        cost=10.0,
        children=[],
        raw={},
    )
    outer = PlanNode(
        node_type="Hash Join",
        relation=None,
        estimated_rows=300,
        actual_rows=None,
        cost=55.0,
        children=[inner],
        raw={},
    )
    return outer


def test_format_leaf_contains_node_type(leaf_node):
    result = format_plan(leaf_node)
    assert "Seq Scan" in result


def test_format_leaf_contains_relation(leaf_node):
    result = format_plan(leaf_node)
    assert "on users" in result


def test_format_leaf_contains_cost(leaf_node):
    result = format_plan(leaf_node)
    assert "cost=42.50" in result


def test_format_leaf_contains_rows(leaf_node):
    result = format_plan(leaf_node)
    assert "rows=1000" in result
    assert "actual=987" in result


def test_format_nested_has_two_lines(nested_plan):
    lines = format_plan(nested_plan).splitlines()
    assert len(lines) == 2


def test_format_nested_root_first(nested_plan):
    lines = format_plan(nested_plan).splitlines()
    assert "Hash Join" in lines[0]


def test_format_nested_child_indented(nested_plan):
    lines = format_plan(nested_plan).splitlines()
    assert lines[1].startswith(" ") or lines[1].startswith("└")
    assert "Seq Scan" in lines[1]


def test_format_nested_child_uses_last_connector(nested_plan):
    lines = format_plan(nested_plan).splitlines()
    assert "└──" in lines[1]


def test_format_no_relation_omitted(nested_plan):
    result = format_plan(nested_plan)
    first_line = result.splitlines()[0]
    assert "on " not in first_line
