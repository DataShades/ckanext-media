"""Tests for views.py."""

import pytest

import ckanext.media.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "media")
@pytest.mark.usefixtures("with_plugins")
def test_media_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("media.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, media!"
