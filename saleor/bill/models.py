from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class Bill(models.Model):
    name = models.CharField(
        pgettext_lazy('Bill field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('Bill field', 'description'), blank=True, null=True)

    updated_at = models.DateTimeField(
        pgettext_lazy('Bill field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('Bill field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'bill'
        verbose_name = pgettext_lazy('Bill model', 'Bill')
        verbose_name_plural = pgettext_lazy('Bills model', 'Bills')

    def __str__(self):
        return self.name




