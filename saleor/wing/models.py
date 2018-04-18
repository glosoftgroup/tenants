from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class Wing(models.Model):
    name = models.CharField(
        pgettext_lazy('Wing field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('Wing field', 'description'), blank=True, null=True)

    updated_at = models.DateTimeField(
        pgettext_lazy('Wing field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('AcademicYear field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'wing'
        verbose_name = pgettext_lazy('Wing model', 'Wing')
        verbose_name_plural = pgettext_lazy('Wings model', 'Wings')

    def __str__(self):
        return self.name




