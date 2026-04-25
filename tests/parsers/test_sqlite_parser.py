from __future__ import annotations

import pytest

from sqlens.parsers.sqlite import SQLitePlanParser
from sqlens.parsers.base import PlanNode, is_leaf, total_nodes


@pytest.fixture
def parser() -> SQLitePlanParser:
    return SQLitePlanParser()


def test_dialect(parser):
    assert parser.dialect == "sqlite"


def test_parse_string_single_node(parser):
    plan_str = "1  0  0  SCAN TABLE users"
    root = parser.parse(plan_str)
    assert isinstance(root, PlanNode)
    assert root.node_type == "Scan"
    assert "SCAN TABLE users" in root.detail
    assert is_leaf(root)
    assert total_nodes(root) == 1


def test_parse_string_nested(parser):
    plan_str = (
        "1  0  0  SCAN TABLE orders\n"
        "2  1  0  SEARCH TABLE users USING INDEX idx_users_id (id=?)\n"
    )
    root = parser.parse(plan_str)
    assert total_nodes(root) == 2
    assert not is_leaf(root)
    child = root.children[0]
    assert child.node_type == "Search"


def test_parse_list_of_tuples(parser):
    rows = [
        (1, 0, 0, "SCAN TABLE products"),
        (2, 1, 0, "USE TEMP B-TREE FOR ORDER BY"),
    ]
    root = parser.parse(rows)
    assert total_nodes(root) == 2
    assert root.node_type == "Scan"
    assert root.children[0].node_type == "UseTempB-Tree"


def test_parse_list_of_dicts(parser):
    rows = [
        {"id": 1, "parent": 0, "notused": 0, "detail": "SCAN TABLE items"},
        {"id": 2, "parent": 1, "notused": 0, "detail": "SEARCH TABLE categories USING INTEGER PRIMARY KEY (rowid=?)"},
    ]
    root = parser.parse(rows)
    assert total_nodes(root) == 2
    assert root.extra["id"] == 1
    assert root.children[0].extra["parent"] == 1


def test_parse_empty_raises(parser):
    with pytest.raises(ValueError, match="Empty plan input"):
        parser.parse([])


def test_parse_blank_string_raises(parser):
    with pytest.raises(ValueError, match="Empty plan input"):
        parser.parse("   \n  ")


def test_parse_skips_blank_lines(parser):
    plan_str = "\n\n1  0  0  SCAN TABLE logs\n\n"
    root = parser.parse(plan_str)
    assert root.node_type == "Scan"
    assert total_nodes(root) == 1


def test_extract_type_fallback(parser):
    # A detail string that doesn't match any keyword should give "Step"
    rows = [(1, 0, 0, "COMPOUND SUBQUERIES 1 AND 2 USING TEMP B-TREE (UNION)")]
    root = parser.parse(rows)
    assert root.node_type == "CompoundSubqueries"
