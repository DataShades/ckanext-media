from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.types import AuthResult, Context, DataDict

from ckanext.media.model.media import MediaModel


def media_list(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


@tk.auth_allow_anonymous_access
def view_media(context: Context, data_dict: DataDict) -> AuthResult:
    media_id = tk.get_or_bust(data_dict, "id")

    media = MediaModel.get_by_id(media_id)

    if not media:
        return {"success": False}

    return {"success": True}


def create_media(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def edit_media(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}


def delete_media(context: Context, data_dict: DataDict) -> AuthResult:
    return {"success": False}
