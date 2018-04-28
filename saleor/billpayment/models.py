from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils.translation import pgettext_lazy
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.timezone import now
from saleor.bill.models import Bill
from saleor.customer.models import Customer
from saleor.room.models import Room
from saleor.paymentoptions.models import PaymentOptions


class BillPayment(models.Model):
    ''' invoice_number for generating invoices of that bill '''
    invoice_number = models.CharField(
        pgettext_lazy('BillPayment field', 'invoice_number'), unique=True, null=True, max_length=36)
    name = models.CharField(
        pgettext_lazy('BillPayment field', 'name'), unique=True, max_length=128)
    description = models.TextField(
        verbose_name=pgettext_lazy('BillPayment field', 'description'), blank=True, null=True)
    bill = models.ForeignKey(
        Bill, blank=True, null=True, related_name='billpayment_types',
        verbose_name=pgettext_lazy('BillPayment field', 'customer'), on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='billpayment_customers',
        verbose_name=pgettext_lazy('BillPayment field', 'customer'), on_delete=models.SET_NULL)
    room = models.ForeignKey(
        Room, blank=True, null=True, related_name='billpayment_rooms',
        verbose_name=pgettext_lazy('BillPayment field', 'room'), on_delete=models.SET_NULL)
    payment_option = models.ForeignKey(
        PaymentOptions, blank=True, null=True, related_name='billpayment_rooms',
        verbose_name=pgettext_lazy('BillPayment field', 'room'), on_delete=models.SET_NULL)
    transaction_number = models.CharField(
        pgettext_lazy('BillPayment field', 'transaction_number'), null=True, max_length=128)

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




