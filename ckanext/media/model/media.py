import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from typing_extensions import Self
from typing import Any

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.model.types import make_uuid

from ckanext.media import types as media_types


class MediaModel(tk.BaseModel):
    __tablename__ = "media"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Text, nullable=False)
    file = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    key = sa.Column(sa.String)
    created = sa.Column(sa.DateTime, server_default=sa.func.now())
    modified = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    extras = sa.Column(MutableDict.as_mutable(JSONB))

    @classmethod
    def get_by_id(cls, id: str) -> Self | None:
        return model.Session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_filename(cls, file: str) -> Self | None:
        return model.Session.query(cls).filter(cls.file == file).first()

    @classmethod
    def get_by_key(cls, key: str) -> Self | None:
        return model.Session.query(cls).filter(cls.key == key).first()

    @classmethod
    def get_by_type(cls, type: str) -> list[Self]:
        return (
            model.Session.query(cls)
            .filter(cls.type == type)
            .order_by(cls.modified.desc())
            .all()
        )

    @classmethod
    def get_all(cls) -> list[Self]:
        return model.Session.query(cls).order_by(cls.modified.desc()).all()

    @classmethod
    def create(cls, data_dict: dict[str, Any]) -> Self:
        media = cls(**data_dict)

        model.Session.add(media)
        model.Session.commit()

        return media

    def delete(self) -> None:
        model.Session().autoflush = False
        model.Session.delete(self)
        model.Session.commit()

    def update(self, data_dict: dict[str, Any]) -> None:
        for key, value in data_dict.items():
            setattr(self, key, value)
        model.Session.commit()

    def dictize(self, context: types.Context) -> media_types.Media:
        return media_types.Media(
            id=str(self.id),
            title=str(self.title),
            file=str(self.file),
            type=str(self.type),
            author=str(self.author),
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
            extras=self.extras,  # type: ignore
            key=self.key, # type: ignore
        )
