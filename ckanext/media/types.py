from typing import Any, TypedDict


class Media(TypedDict):
    id: str
    title: str
    file: str
    type: str
    author: str
    created: str
    modified: str
    extras: dict[str, Any]
    key: str | None
