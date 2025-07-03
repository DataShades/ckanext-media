from __future__ import annotations

from typing import Any
from sqlalchemy import or_
import mimetypes

import ckan.plugins.toolkit as tk
import ckan.types as types
import ckan.lib.uploader as uploader

from ckanext.media.model.media import MediaModel
from ckanext.media import config


def upload_media_to_storage(key, data, errors, context):
    file_data = data.get(key)
    if isinstance(file_data, str):
        if file_data.startswith("<") and file_data.endswith(">"):
            errors[key].append("Re-upload the file.")
        return

    try:
        media_type = data.get(("type",))
        if not media_type:
            errors[key].append("Missing media type.")

        types = config.media_get_types()

        try:
            type = types[media_type]
        except KeyError:
            errors[key].append("No such type.")

        mimetype = mimetypes.guess_type(file_data.filename)
        if mimetype[0] not in type["allowed_mimetypes"]:
            errors[key].append(
                "File with mimetype '{mime}' is not allowed.".format(mime=mimetype[0])
            )

        upload = uploader.get_uploader("media")
        upload.update_data_dict(data, key, key, "clear_upload")
        upload.upload(type["max_filesize"] if type.get("max_filesize") else 3)
    except (tk.ValidationError, OSError) as e:
        errors[key].append(str(e))

    return


def media_key_is_unique(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Ensures that the media with a given key doesn't exist"""

    val = data[key]
    if val:
        id = data.get(("id",))
        media = MediaModel.get_by_key(val)
        if media:
            if not id:
                raise tk.Invalid(f"The key '{val}' already exists.")

            if int(id) != media.id:
                raise tk.Invalid(f"The key '{val}' already exists.")

    return


def media_exists(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    val = data[key]
    if val:
        media = MediaModel.find_media(val)

        if not media:
            raise tk.Invalid(f"Media does not exist.")

    return
