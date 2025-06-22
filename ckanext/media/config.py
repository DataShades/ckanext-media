import ckan.plugins.toolkit as tk

MEDIA_DEFAULT_TYPES = ["image|Image", "file|File"]
MEDIA_EXTRA_TYPES = "ckanext.media.extra_types"


def media_get_types() -> dict[str, str]:
    configs = [MEDIA_DEFAULT_TYPES, tk.config.get(MEDIA_EXTRA_TYPES)]
    types = {}
    for config in configs:
        if config:
            types = types | {
            type_: label
            for type_, label in (item.split('|') for item in config if config)
            }

    return types
