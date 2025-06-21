import ckan.plugins.toolkit as tk
import ckanext.media.logic.schema as schema


@tk.side_effect_free
def media_get_sum(context, data_dict):
    tk.check_access(
        "media_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.media_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'media_get_sum': media_get_sum,
    }
