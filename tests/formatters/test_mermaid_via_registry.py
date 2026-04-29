"""Integration test: obtain the Mermaid formatter via the registry and render."""

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter


@pytest.fixture
def simple_plan() -> PlanNode:
    child = PlanNode(
        node_type="Seq Scan",
        relation="products",
        estimated_cost=8.0,
        actual_rows=100,
        children=[],
        extra={},
    )
    return PlanNode(
        node_type="Aggregate",
        relation=None,
        estimated_cost=25.0,
        actual_rows=1,
        children=[child],
        extra={},
    )


def test_registry_returns_mermaid_formatter():
    mod = get_formatter("mermaid")
    assert mod.__name__.endswith("mermaid")


def test_registry_mermaid_format_plan_callable():
    mod = get_formatter("mermaid")
    assert callable(mod.format_plan)


def test_registry_mermaid_renders_graph(simple_plan):
    mod = get_formatter("mermaid")
    result = mod.format_plan(simple_plan)
    assert "graph TD" in result
    assert "Aggregate" in result
    assert "Seq Scan" in result


def test_registry_mermaid_renders_edge(simple_plan):
    mod = get_formatter("mermaid")
    result = mod.format_plan(simple_plan)
    assert "-->" in result


def test_registry_mermaid_output_ends_with_newline(simple_plan):
    mod = get_formatter("mermaid")
    result = mod.format_plan(simple_plan)
    assert result.endswith("\n")
