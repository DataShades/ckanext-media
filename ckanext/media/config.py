from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
from ckan.common import _
import ckan.plugins as p

from ckanext.media import interfaces

ALLOWED_IMAGE_MIMETYPES = "ckanext.media.image.allowed_mimetypes"
ALLOWED_FILE_MIMETYPES = "ckanext.media.file.allowed_mimetypes"

IMAGE_MAX_FILESIZE = "ckanext.media.image.max_filesize"
FILE_MAX_FILEZE = "ckanext.media.file.max_filesize"


def media_get_types() -> dict[str, Any]:
    types = {
        "image": {
            "label": _("Image"),
            "allowed_mimetypes": tk.config.get(ALLOWED_IMAGE_MIMETYPES),
            "max_filesize": tk.config.get(IMAGE_MAX_FILESIZE),
        },
        "file": {
            "label": _("File"),
            "allowed_mimetypes": tk.config.get(ALLOWED_FILE_MIMETYPES),
            "max_filesize": tk.config.get(FILE_MAX_FILEZE),
        },
    }

    # additional types registration
    for item in p.PluginImplementations(interfaces.IMedia):
        item.media_types(types)

    return types
