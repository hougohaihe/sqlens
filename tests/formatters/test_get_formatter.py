"""Tests for the formatters registry / get_formatter helper."""

from __future__ import annotations

import pytest

from sqlens.formatters import get_formatter
from sqlens.formatters import text, json_fmt


def test_get_formatter_text_returns_text_module():
    assert get_formatter("text") is text


def test_get_formatter_json_returns_json_module():
    assert get_formatter("json") is json_fmt


def test_get_formatter_unknown_raises_value_error():
    with pytest.raises(ValueError, match="Unknown formatter"):
        get_formatter("xml")


def test_get_formatter_error_message_lists_supported():
    with pytest.raises(ValueError, match="json"):
        get_formatter("nope")


def test_text_formatter_has_format_plan():
    assert callable(getattr(text, "format_plan", None))


def test_json_formatter_has_format_plan():
    assert callable(getattr(json_fmt, "format_plan", None))
