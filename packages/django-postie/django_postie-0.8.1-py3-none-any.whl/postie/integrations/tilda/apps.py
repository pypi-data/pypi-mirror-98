from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class PostieTildaConfig(AppConfig):
    name = 'postie.integrations.tilda'
    verbose_name = pgettext_lazy(
        'Postie integrations tilda app', 'Postie tilda'
    )
