from flask import Blueprint


media = Blueprint(
    "media", __name__)


def page():
    return "Hello, media!"


media.add_url_rule(
    "/media/page", view_func=page)


def get_blueprints():
    return [media]
