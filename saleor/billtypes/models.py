from __future__ import unicode_literals

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now
from decimal import Decimal
from django.core.validators import MinValueValidator, RegexValidator

class BillTypes(models.Model):
    name = models.CharField(
        pgettext_lazy('BillTypes field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('BillTypes field', 'description'), blank=True, null=True)
    tax = models.DecimalField(
        pgettext_lazy('BillTypes field', 'tax field'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)

    updated_at = models.DateTimeField(
        pgettext_lazy('BillTypes field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('BillTypes field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'billtypes'
        verbose_name = pgettext_lazy('BillTypes model', 'BillTypes')
        verbose_name_plural = pgettext_lazy('BillTypes model', 'BillTypes')

    def __str__(self):
        return self.name




