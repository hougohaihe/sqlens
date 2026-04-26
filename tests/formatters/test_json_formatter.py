"""Tests for the JSON plan formatter."""

from __future__ import annotations

import json

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.json import format_plan, _node_to_dict


@pytest.fixture()
def leaf_node() -> PlanNode:
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        estimated_cost=4.5,
        actual_rows=10,
        extra={"filter": "age > 18"},
        children=[],
    )


@pytest.fixture()
def nested_plan() -> PlanNode:
    inner = PlanNode(
        node_type="Index Scan",
        relation="orders",
        estimated_cost=1.0,
        actual_rows=5,
        extra={},
        children=[],
    )
    return PlanNode(
        node_type="Hash Join",
        relation=None,
        estimated_cost=12.0,
        actual_rows=5,
        extra={"hash_cond": "(users.id = orders.user_id)"},
        children=[inner],
    )


def test_format_plan_returns_valid_json(leaf_node):
    output = format_plan(leaf_node)
    parsed = json.loads(output)  # must not raise
    assert isinstance(parsed, dict)


def test_format_plan_contains_node_type(leaf_node):
    output = format_plan(leaf_node)
    data = json.loads(output)
    assert data["node_type"] == "Seq Scan"


def test_format_plan_contains_relation(leaf_node):
    data = json.loads(format_plan(leaf_node))
    assert data["relation"] == "users"


def test_format_plan_omits_relation_when_none(nested_plan):
    data = json.loads(format_plan(nested_plan))
    assert "relation" not in data


def test_format_plan_contains_cost(leaf_node):
    data = json.loads(format_plan(leaf_node))
    assert data["estimated_cost"] == pytest.approx(4.5)


def test_format_plan_contains_extra(leaf_node):
    data = json.loads(format_plan(leaf_node))
    assert data["extra"] == {"filter": "age > 18"}


def test_format_plan_nested_children(nested_plan):
    data = json.loads(format_plan(nested_plan))
    assert len(data["children"]) == 1
    child = data["children"][0]
    assert child["node_type"] == "Index Scan"
    assert child["relation"] == "orders"


def test_format_plan_leaf_has_no_children_key(leaf_node):
    """Children key should be absent for leaf nodes to keep output clean."""
    data = json.loads(format_plan(leaf_node))
    assert "children" not in data


def test_format_plan_custom_indent(leaf_node):
    output = format_plan(leaf_node, indent=4)
    # 4-space indent means lines start with at least 4 spaces
    lines = output.splitlines()
    indented = [l for l in lines if l.startswith(" ")]
    assert all(l.startswith("    ") for l in indented)


def test_node_to_dict_omits_empty_extra(leaf_node):
    leaf_node.extra = {}
    result = _node_to_dict(leaf_node)
    assert "extra" not in result
