from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

Schema = Dict[str, Any]


@validator_args
def create_media(
    not_empty,
    unicode_safe,
    ignore,
    default,
    upload_media_to_storage,
) -> Schema:

    return {
        "title": [not_empty, unicode_safe],
        "type": [not_empty, unicode_safe],
        "file": [not_empty, upload_media_to_storage],
        "extras": [ignore, unicode_safe],
        "key": [default(''), unicode_safe],
    }


@validator_args
def update_media(
    not_empty,
    unicode_safe,
    ignore,
    default,
    upload_media_to_storage,
) -> Schema:

    return {
        "id": [not_empty],
        "title": [not_empty, unicode_safe],
        "type": [not_empty, unicode_safe],
        "file": [not_empty, upload_media_to_storage],
        "extras": [ignore, unicode_safe],
        "key": [default(''), unicode_safe],
    }
