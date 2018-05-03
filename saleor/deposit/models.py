from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now
from django_prices.models import PriceField
from django.core.validators import MinValueValidator, RegexValidator
from saleor.billtypes.models import BillTypes
from saleor.customer.models import Customer
from saleor.room.models import Room


class Deposit(models.Model):
    ''' invoice_number for generating invoices of that bill '''
    invoice_number = models.CharField(
        pgettext_lazy('Deposit field', 'invoice_number'), unique=True, null=True, max_length=36)
    name = models.CharField(
        pgettext_lazy('Deposit field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('Deposit field', 'description'), blank=True, null=True)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='deposit_customers',
        verbose_name=pgettext_lazy('Deposit field', 'customer'), on_delete=models.SET_NULL)
    room = models.ForeignKey(
        Room, blank=True, null=True, related_name='deposit_rooms',
        verbose_name=pgettext_lazy('Deposit field', 'room'), on_delete=models.SET_NULL)
    deposit_months = models.IntegerField(default=Decimal(1))
    amount = models.DecimalField(
        pgettext_lazy('Deposit field', 'total deposit amount'), default=Decimal(0), max_digits=19, decimal_places=5)

    month = models.DateField(
        pgettext_lazy('Deposit field', 'month billed'),
        default=now)
    status = models.CharField(
        pgettext_lazy('Deposit field', 'status'), default='pending', null=True, max_length=128)

    updated_at = models.DateTimeField(
        pgettext_lazy('Deposit field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('Deposit field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'deposit'
        verbose_name = pgettext_lazy('Deposit model', 'Deposit')
        verbose_name_plural = pgettext_lazy('Deposits model', 'Deposits')

    def __str__(self):
        return self.name




