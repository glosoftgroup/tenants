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


class Bill(models.Model):
    ''' invoice_number for generating invoices of that bill '''
    invoice_number = models.CharField(
        pgettext_lazy('Bill field', 'invoice_number'), default='', null=True, max_length=36)
    description = models.TextField(
        verbose_name=pgettext_lazy('Bill field', 'description'), blank=True, null=True)
    billtype = models.ForeignKey(
        BillTypes, blank=True, null=True, related_name='bill_types',
        verbose_name=pgettext_lazy('Bill field', 'customer'), on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='bill_customers',
        verbose_name=pgettext_lazy('Bill field', 'customer'), on_delete=models.SET_NULL)
    room = models.ForeignKey(
        Room, blank=True, null=True, related_name='bill_rooms',
        verbose_name=pgettext_lazy('Bill field', 'room'), on_delete=models.SET_NULL)
    amount = models.DecimalField(
        pgettext_lazy('Bill field', 'amount of the bill'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    tax = models.DecimalField(
        pgettext_lazy('Bill field', 'amount of the bill'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    is_taxable = models.BooleanField(
        pgettext_lazy('Book field', 'is taxable'), default=False)
    month = models.DateField(
        pgettext_lazy('Bill field', 'month billed'),
        default=now)
    status = models.CharField(
        pgettext_lazy('Bill field', 'status'), default='pending', null=True, max_length=128) 

    updated_at = models.DateTimeField(
        pgettext_lazy('Bill field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('Bill field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'bill'
        verbose_name = pgettext_lazy('Bill model', 'Bill')
        verbose_name_plural = pgettext_lazy('Bills model', 'Bills')

    def __str__(self):
        return self.billtype.name




