from flask import current_app
from jinja2 import TemplateNotFound

import ckan.plugins.toolkit as tk

from ckanext.media.model.media import MediaModel


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


def uploaded_media_url(filename: str):
    return tk.get_action("get_media_uploaded_url")({}, {"filename": filename})


def get_media_by_key(key):
    media = MediaModel.get_by_key(key)

    if not media:
        return {}

    media_dict = {key: value for key, value in media.dictize({}).items()}

    media_dict['file_url'] = uploaded_media_url(
        media_dict['file'])  # type: ignore

    return media_dict


def get_media_fielurl_by_key(key):
    media = MediaModel.get_by_key(key)

    if not media:
        return {}

    return uploaded_media_url(media.file)  # type: ignore


def get_media_fielurl_by_id(id):
    media = MediaModel.get_by_id(id)
    
    if not media:
        return {}
    
    return uploaded_media_url(media.file) # type: ignore
