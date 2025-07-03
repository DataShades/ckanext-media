from __future__ import annotations

from typing import cast
import six
import os

from ckan.logic import validate
import ckan.plugins.toolkit as tk
import ckan.logic as logic
from ckan import types
import ckan.model as model
import ckan.lib.uploader as uploader

from ckanext.media.model.media import MediaModel
import ckanext.media.logic.schema as schema


ValidationError = logic.ValidationError


@validate(schema.create_media)
def create_media(context, data_dict):
    tk.check_access("create_media", context, data_dict)
    user = context["user"]

    if user:
        user_obj = model.User.by_name(six.ensure_text(user))
        if not user_obj:
            raise logic.ValidationError({"author": [f"Missing Author"]})
        data_dict["author"] = user_obj.id

    media = MediaModel.create(data_dict)
    return media


@validate(schema.update_media)
def edit_media(context, data_dict):
    tk.check_access("edit_media", context, data_dict)
    media = MediaModel.get_by_id(data_dict["id"])

    if not media:
        raise logic.NotFound("No such Media.")

    media = media.update(data_dict)

    return media


@tk.side_effect_free
def get_media_uploaded_url(context: types.Context, data_dict: types.DataDict):
    filename = data_dict.get("filename", "")

    path = "/uploads/media/" + filename

    return tk.h.url_for(path, qualified=True)


def delete_media(context: types.Context, data_dict: types.DataDict) -> bool:
    tk.check_access("delete_media", context, data_dict)

    media = cast(MediaModel, MediaModel.get_by_id(data_dict["id"]))

    filename = media.file
    upload = uploader.get_uploader("media")

    try:
        os.remove(os.path.join(upload.storage_path, filename))  # type: ignore
    except OSError:
        pass

    media.delete()

    return True
