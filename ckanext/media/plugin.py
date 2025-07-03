from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


@toolkit.blanket.validators
@toolkit.blanket.actions
@toolkit.blanket.auth_functions
@toolkit.blanket.helpers
@toolkit.blanket.blueprints
@toolkit.blanket.config_declarations
class MediaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "media")
