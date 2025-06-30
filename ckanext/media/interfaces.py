from __future__ import annotations

from typing import Any

from ckan.plugins import Interface


class IMedia(Interface):
    """Implement custom Media response modification."""

    def media_types(self, media_types: dict[str, Any]) -> dict[str, Any]:
        """Return Dict of media types.
        This method is called after the default media types are ready.
        Needed to register custom Media types.
        :returns: dict
        :rtype: dict

        """

        return media_types
