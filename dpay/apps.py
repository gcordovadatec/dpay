from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "dpay"
    verbose_name = "Dpay"

    class PretixPluginMeta:
        name = gettext_lazy("Dpay")
        author = "Datec LTDA"
        description = gettext_lazy("test description")
        visible = True
        version = __version__
        category = "PAYMENT"
        compatibility = "pretix>=1.0.0"
        settings_links = []
        navigation_links = []

    def ready(self):
        from . import signals  # NOQA
