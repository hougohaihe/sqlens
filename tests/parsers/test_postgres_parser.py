"""Tests for the PostgreSQL plan parser."""

import json
import pytest

from sqlens.parsers.postgres import PostgresPlanParser
from sqlens.parsers.base import PlanNode


SIMPLE_PLAN = [
    {
        "Plan": {
            "Node Type": "Seq Scan",
            "Relation Name": "users",
            "Total Cost": 12.5,
            "Plan Rows": 100,
            "Actual Rows": 98,
            "Actual Total Time": 0.342,
        }
    }
]

NESTED_PLAN = [
    {
        "Plan": {
            "Node Type": "Hash Join",
            "Total Cost": 55.0,
            "Plan Rows": 200,
            "Actual Rows": 195,
            "Actual Total Time": 1.2,
            "Plans": [
                {
                    "Node Type": "Seq Scan",
                    "Relation Name": "orders",
                    "Total Cost": 20.0,
                    "Plan Rows": 500,
                    "Actual Rows": 498,
                    "Actual Total Time": 0.5,
                },
                {
                    "Node Type": "Hash",
                    "Total Cost": 10.0,
                    "Plan Rows": 50,
                    "Actual Rows": 50,
                    "Actual Total Time": 0.1,
                    "Plans": [],
                },
            ],
        }
    }
]


@pytest.fixture
def parser() -> PostgresPlanParser:
    return PostgresPlanParser()


def test_dialect(parser):
    assert parser.dialect == "postgres"


def test_parse_simple_plan(parser):
    root = parser.parse(SIMPLE_PLAN)
    assert isinstance(root, PlanNode)
    assert root.node_type == "Seq Scan"
    assert root.cost == 12.5
    assert root.rows == 100
    assert root.actual_rows == 98
    assert root.actual_time_ms == 0.342
    assert root.is_leaf()
    assert root.total_nodes() == 1


def test_parse_nested_plan(parser):
    root = parser.parse(NESTED_PLAN)
    assert root.node_type == "Hash Join"
    assert not root.is_leaf()
    assert len(root.children) == 2
    assert root.total_nodes() == 3
    assert root.children[0].node_type == "Seq Scan"
    assert root.children[1].node_type == "Hash"


def test_parse_json_string(parser):
    root = parser.parse(json.dumps(SIMPLE_PLAN))
    assert root.node_type == "Seq Scan"


def test_details_excludes_reserved_keys(parser):
    root = parser.parse(SIMPLE_PLAN)
    assert "Node Type" not in root.details
    assert "Total Cost" not in root.details
    assert "Relation Name" in root.details


def test_plan_node_repr(parser):
    root = parser.parse(SIMPLE_PLAN)
    assert "Seq Scan" in repr(root)
    assert "cost=" in repr(root)
