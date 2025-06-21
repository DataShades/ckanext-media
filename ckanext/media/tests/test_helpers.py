"""Tests for helpers.py."""

import ckanext.media.helpers as helpers


def test_media_hello():
    assert helpers.media_hello() == "Hello, media!"
