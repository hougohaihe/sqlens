"""Tests for the formatter registry."""

import pytest

from sqlens.formatters import get_formatter
from sqlens.formatters import text as text_mod
from sqlens.formatters import json as json_mod
from sqlens.formatters import html as html_mod
from sqlens.formatters import markdown as markdown_mod
from sqlens.formatters import mermaid as mermaid_mod


def test_get_formatter_text_returns_text_module():
    assert get_formatter("text") is text_mod


def test_get_formatter_json_returns_json_module():
    assert get_formatter("json") is json_mod


def test_get_formatter_html_returns_html_module():
    assert get_formatter("html") is html_mod


def test_get_formatter_markdown_returns_markdown_module():
    assert get_formatter("markdown") is markdown_mod


def test_get_formatter_mermaid_returns_mermaid_module():
    assert get_formatter("mermaid") is mermaid_mod


def test_get_formatter_unknown_raises_value_error():
    with pytest.raises(ValueError, match="Unknown formatter"):
        get_formatter("xml")


def test_get_formatter_error_message_lists_supported():
    with pytest.raises(ValueError, match="mermaid"):
        get_formatter("csv")


def test_get_formatter_case_sensitive():
    with pytest.raises(ValueError):
        get_formatter("Text")


def test_get_formatter_mermaid_has_format_plan():
    mod = get_formatter("mermaid")
    assert callable(getattr(mod, "format_plan", None))
