from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView
from sqlalchemy import or_


import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
from ckan.types import Context
import ckan.model as model
from ckan.lib.helpers import Page, pager_url

from ckanext.media.model.media import MediaModel
from ckanext.media import config


ValidationError = logic.ValidationError

media = Blueprint("media", __name__)

BASE_FIELDS = [
    "title",
    "type",
    "file",
    "key",
]


def make_context() -> Context:
    return {
        "user": tk.current_user.name,
        "auth_user_obj": tk.current_user,
    }


class CreateView(MethodView):
    def get(self, type):
        try:
            tk.check_access("create_media", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        types = config.media_get_types()

        if type not in types:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        extra_vars = {
            "types": types,
            "form_data": form_data,
            "errors": {},
            "type": type,
        }

        template = tk.h.guess_media_type_create_snippet(type)
        return tk.render(template, extra_vars=extra_vars)

    def post(self, type):
        try:
            tk.check_access("create_media", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        types = config.media_get_types()

        if type not in types:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        for f_name, file in tk.request.files.items():
            correct_key = f_name.split("_media-")
            if file.filename and len(correct_key) and correct_key[1] == "upload":
                form_data[correct_key[0]] = file

        form_data["extras"] = {}
        form_data["type"] = type

        for field in form_data:
            if field == "extras":
                continue
            if field not in BASE_FIELDS:
                form_data["extras"][field] = form_data.pop(field)

        try:
            tk.get_action("create_media")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            template = tk.h.guess_media_type_create_snippet(type)
            return tk.render(
                template,
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("media.list")


class EditView(MethodView):
    def get(self, type: str, id: str):
        media = MediaModel.get_by_id(id)

        try:
            tk.check_access("edit_media", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not media:
            return tk.abort(404, "Page not found")

        form_data = media.dictize({})

        return tk.render(
            "media/edit.html",
            extra_vars={
                "type": type,
                "id": id,
                "form_data": form_data,
                "errors": {},
            },
        )

    def post(self, type, id: str):
        try:
            tk.check_access("edit_media", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        types = config.media_get_types()

        if type not in types:
            return tk.abort(404, "Page not found")

        try:
            form_data = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(logic.parse_params(tk.request.form))
                )
            )
        except dict_fns.DataError:
            return tk.base.abort(400, tk._("Integrity Error"))

        for f_name, file in tk.request.files.items():
            correct_key = f_name.split("_media-")
            if file.filename and len(correct_key) and correct_key[1] == "upload":
                form_data[correct_key[0]] = file

        form_data["extras"] = {}
        form_data["type"] = type

        for field in form_data:
            if field == "extras":
                continue
            if field not in BASE_FIELDS:
                form_data["extras"][field] = form_data.pop(field)

        form_data["id"] = id

        try:
            tk.get_action("edit_media")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            template = tk.h.guess_media_type_create_snippet(type)
            return tk.render(
                template,
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("media.list")


class DeleteView(MethodView):
    def get(self, type: str, id: str):
        media = MediaModel.get_by_id(id)

        try:
            tk.check_access("delete_media", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        if not media:
            return tk.abort(404, "Page not found")

        form_data = media.dictize({})

        return tk.render(
            "media/delete.html",
            extra_vars={
                "type": type,
                "id": id,
                "form_data": form_data,
                "errors": {},
            },
        )

    def post(self, type, id: str):
        try:
            tk.check_access("delete_media", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        types = config.media_get_types()

        if type not in types:
            return tk.abort(404, "Page not found")

        form_data = {"id": id}

        try:
            tk.get_action("delete_media")(make_context(), form_data)
        except logic.ValidationError as e:
            tk.h.flash_error(e.error_summary)
            return tk.render(
                "media/delete.html",
                extra_vars={"form_data": form_data, "errors": {}},
            )

        return tk.redirect_to("media.list")


class ReadView(MethodView):
    def _check_access(self, type: str, id: str):
        try:
            tk.check_access("view_media", make_context(), {"id": id})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

    def get(self, type: str, id: str):
        media = MediaModel.get_by_id(id)

        if not media:
            return tk.abort(404, "Page not found")

        self._check_access(type, id)

        template = tk.h.guess_media_type_snippet(type)
        return tk.render(
            template,
            extra_vars={
                "type": type,
                "id": id,
                "media": media.dictize({}),
            },
        )


class ListView(MethodView):
    def get(self):
        types = config.media_get_types()

        try:
            tk.check_access("create_media", make_context(), {})
        except tk.NotAuthorized:
            return tk.abort(404, "Page not found")

        extra_vars = {}
        extra_vars["q"] = q = tk.request.args.get("q", "")
        extra_vars["type"] = type = tk.request.args.get("type", "")
        page = tk.h.get_page_number(tk.request.args)
        limit = 20

        query = model.Session.query(MediaModel)

        if q:
            query = query.filter(
                or_(
                    MediaModel.title.ilike("%" + q.strip() + "%"),
                    MediaModel.key.ilike("%" + q.strip() + "%"),
                    MediaModel.file.ilike("%" + q.strip() + "%"),
                )
            )

        if type:
            query = query.filter_by(type=type)

        extra_vars["count"] = count = query.count()

        query = (
            query.order_by(MediaModel.modified.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        medias = [item.dictize({}) for item in query]

        extra_vars["page"] = Page(
            collection=medias,
            page=page,
            url=pager_url,
            item_count=count,
            items_per_page=limit,
        )
        extra_vars["page"].items = medias
        extra_vars["types"] = types

        return tk.render("media/list.html", extra_vars=extra_vars)


@media.route("/media-widget-list/<media_type>")
def media_widget_list(media_type):

    medias = (
        model.Session.query(MediaModel)
        .filter(MediaModel.type == media_type)
        .order_by(MediaModel.modified.desc())
        .limit(12)
        .all()
    )

    template = tk.h.media_type_widget_template(media_type)
    return tk.render(
        "media/widget/media_modal_list.html",
        extra_vars={"medias": medias, "template": template},
    )


@media.route("/media-widget-search/<media_type>", methods=["POST"])
def media_widget_search(media_type):
    try:
        form_data = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(tk.request.form)))
        )
    except dict_fns.DataError:
        return tk.base.abort(400, tk._("Integrity Error"))

    search = form_data.get("search", "")

    medias = model.Session.query(MediaModel).filter(MediaModel.type == media_type)
    if search:
        medias = medias.filter(
            or_(
                MediaModel.title.ilike("%" + search.strip() + "%"),
                MediaModel.key.ilike("%" + search.strip() + "%"),
                MediaModel.file.ilike("%" + search.strip() + "%"),
            )
        )

    medias = medias.order_by(MediaModel.modified.desc()).limit(12).all()
    return tk.render(
        "media/widget/media_modal_list.html", extra_vars={"medias": medias}
    )


media.add_url_rule("/media/list", view_func=ListView.as_view("list"))
media.add_url_rule("/media/<type>/create", view_func=CreateView.as_view("create"))
media.add_url_rule("/media/<type>/edit/<id>", view_func=EditView.as_view("edit"))
media.add_url_rule("/media/<type>/delete/<id>", view_func=DeleteView.as_view("delete"))
media.add_url_rule("/media/<type>/<id>", view_func=ReadView.as_view("read"))
