"""Tests for the formatter registry (get_formatter)."""

import pytest
from sqlens.formatters import get_formatter
from sqlens.formatters import text as text_module
from sqlens.formatters import json as json_module
from sqlens.formatters import html as html_module
from sqlens.formatters import markdown as markdown_module


def test_get_formatter_text_returns_text_module():
    assert get_formatter("text") is text_module


def test_get_formatter_json_returns_json_module():
    assert get_formatter("json") is json_module


def test_get_formatter_html_returns_html_module():
    assert get_formatter("html") is html_module


def test_get_formatter_markdown_returns_markdown_module():
    assert get_formatter("markdown") is markdown_module


def test_get_formatter_unknown_raises_value_error():
    with pytest.raises(ValueError):
        get_formatter("xml")


def test_get_formatter_error_message_lists_supported():
    with pytest.raises(ValueError, match="text"):
        get_formatter("csv")


def test_text_formatter_has_format_plan():
    assert hasattr(get_formatter("text"), "format_plan")


def test_markdown_formatter_has_format_plan():
    assert hasattr(get_formatter("markdown"), "format_plan")
