from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class BillPayment(models.Model):
    name = models.CharField(
        pgettext_lazy('BillPayment field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('BillPayment field', 'description'), blank=True, null=True)

    updated_at = models.DateTimeField(
        pgettext_lazy('BillPayment field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('BillPayment field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'billpayment'
        verbose_name = pgettext_lazy('BillPayment model', 'BillPayment')
        verbose_name_plural = pgettext_lazy('BillPayments model', 'BillPayments')

    def __str__(self):
        return self.name




