"""Tests for the HTML formatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import html as html_formatter
from sqlens.formatters.html import format_plan


@pytest.fixture
def leaf_node():
    return PlanNode(
        node_type="Seq Scan",
        relation="users",
        cost=12.5,
        rows=100,
        children=[],
    )


@pytest.fixture
def nested_plan():
    inner = PlanNode(node_type="Index Scan", relation="orders", cost=4.2, rows=10, children=[])
    outer = PlanNode(node_type="Hash Join", relation=None, cost=30.0, rows=50, children=[inner])
    return outer


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
    assert "rows=100" in result


def test_format_plan_wraps_in_div(leaf_node):
    result = format_plan(leaf_node)
    assert result.startswith("<div class='sqlens-plan'>")
    assert result.strip().endswith("</div>")


def test_format_plan_includes_style_tag(leaf_node):
    result = format_plan(leaf_node)
    assert "<style>" in result
    assert "</style>" in result


def test_format_plan_nested_contains_all_nodes(nested_plan):
    result = format_plan(nested_plan)
    assert "Hash Join" in result
    assert "Index Scan" in result
    assert "orders" in result


def test_format_plan_nested_uses_ul(nested_plan):
    result = format_plan(nested_plan)
    assert "<ul>" in result
    assert "<li>" in result


def test_html_formatter_module_has_format_plan():
    assert hasattr(html_formatter, "format_plan")
    assert callable(html_formatter.format_plan)
