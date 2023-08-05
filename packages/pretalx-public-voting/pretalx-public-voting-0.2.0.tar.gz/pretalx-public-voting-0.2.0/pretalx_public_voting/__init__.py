from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class PluginApp(AppConfig):
    name = "pretalx_public_voting"
    verbose_name = "pretalx public voting plugin"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx public voting plugin")
        author = "Tobias Kunze"
        description = gettext_lazy("A public voting plugin for pretalx")
        visible = True
        version = "0.2.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretalx_public_voting.PluginApp"
