from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class PaymentOptions(models.Model):
    name = models.CharField(
        pgettext_lazy('PaymentOptions field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('PaymentOptions field', 'description'), blank=True, null=True)

    updated_at = models.DateTimeField(
        pgettext_lazy('PaymentOptions field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('PaymentOptions field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'paymentoptions'
        verbose_name = pgettext_lazy('PaymentOption model', 'PaymentOption')
        verbose_name_plural = pgettext_lazy('PaymentOptions model', 'PaymentOptions')

    def __str__(self):
        return self.name




