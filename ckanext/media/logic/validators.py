from typing import Any
import re

import ckan.plugins.toolkit as tk
import ckan.types as types
import ckan.lib.uploader as uploader

# from ckanext.content.model.content import ContentModel

def upload_media_to_storage(key, data, errors, context):
    file_data = data.get(key)

    if isinstance(file_data, str):
        return
    try:
        upload = uploader.get_uploader("media")
        upload.update_data_dict(data, key, key, "clear_upload")
        upload.upload(uploader.get_max_image_size())
    except (tk.ValidationError, OSError) as e:
        raise tk.Invalid(str(e))
