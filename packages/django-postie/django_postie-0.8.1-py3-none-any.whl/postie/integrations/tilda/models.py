from django.utils.translation import pgettext_lazy
from django.db import models
from solo.models import SingletonModel


class Preferences(SingletonModel):
    public_key = models.CharField(
        verbose_name=pgettext_lazy('tilda preferences model', 'Public key'),
        max_length=255
    )
    private_key = models.CharField(
        verbose_name=pgettext_lazy('tilda preferences model', 'Private key'),
        max_length=255
    )
    project_id = models.PositiveIntegerField(
        verbose_name=pgettext_lazy('tilda preferences model', 'Project id'),
        null=True
    )

    class Meta:
        verbose_name = pgettext_lazy('tilda preferences model', 'Preferences')
