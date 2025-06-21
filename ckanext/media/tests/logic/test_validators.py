"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.media.logic import validators


def test_media_reauired_with_valid_value():
    assert validators.media_required("value") == "value"


def test_media_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.media_required(None)
