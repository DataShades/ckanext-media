from __future__ import annotations

from flask import current_app
from jinja2 import TemplateNotFound
from markupsafe import Markup

import ckan.plugins.toolkit as tk

from ckanext.media.model.media import MediaModel
from ckanext.media import config


def guess_media_type_snippet(type):
    env = current_app.jinja_env
    default_path = "media/display/"

    path = default_path + "read_" + type + ".html"
    try:
        env.get_template(path)
        return path
    except TemplateNotFound:
        return default_path + "read.html"


def guess_media_type_create_snippet(type):
    env = current_app.jinja_env
    default_path = "media/"

    path = default_path + "create_" + type + ".html"
    try:
        env.get_template(path)
        return path
    except TemplateNotFound:
        return default_path + "create.html"


def guess_media_type_preview_snippet(type):
    env = current_app.jinja_env
    default_path = "media/snippets/preview/"

    path = default_path + "media_" + type + ".html"
    try:
        env.get_template(path)
        return path
    except TemplateNotFound:
        return default_path + "media.html"


def media_type_widget_template(type):
    env = current_app.jinja_env
    default_path = "media/widget/type/"

    path = default_path + type + ".html"
    try:
        env.get_template(path)
        return path
    except TemplateNotFound:
        return default_path + "default.html"


def get_media_fileurl_by_filename(filename: str):
    return tk.get_action("get_media_uploaded_url")({}, {"filename": filename})


def get_media_by_key(key):
    media = MediaModel.get_by_key(key)

    if not media:
        return {}

    media_dict = {key: value for key, value in media.dictize({}).items()}

    media_dict["file_url"] = get_media_fileurl_by_filename(
        media_dict["file"])  # type: ignore

    return media_dict


def get_media_fileurl_by_key(key):
    media = MediaModel.get_by_key(key)

    if not media:
        return ""

    return get_media_fileurl_by_filename(media.file)  # type: ignore


def get_media_fileurl_by_id(id):
    media = MediaModel.get_by_id(id)

    if not media:
        return ""

    return get_media_fileurl_by_filename(media.file)  # type: ignore


def find_media(value):
    return MediaModel.find_media(value)


def media_types_preview_templates():
    media_types = config.media_get_types()

    preview_templates = {
        i: tk.h.guess_media_type_preview_snippet(i) for i in media_types}

    return preview_templates
