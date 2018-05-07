from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from decimal import Decimal
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.timezone import now
from saleor.bill.models import Bill
from saleor.customer.models import Customer
from saleor.room.models import Room
from saleor.paymentoptions.models import PaymentOptions


class BillPaymentManager(BaseUserManager):
    def room_total_payment(self, room, billtype=None):
        query = self.get_queryset()
        if room:
            query = query.filter(room=room)
        if billtype:
            query = query.filter(billtype__name=billtype)
        return query.aggregate(models.Sum('amount'))['amount__sum']


class BillPayment(models.Model):
    ''' invoice_number for generating invoices of that bill '''
    invoice_number = models.CharField(
        pgettext_lazy('BillPayment field', 'invoice_number'), null=True, max_length=36)
    bill = models.ForeignKey(
        Bill, blank=True, null=True, related_name='billpayment',
        verbose_name=pgettext_lazy('BillPayment field', 'customer'), on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='billpayment_customers',
        verbose_name=pgettext_lazy('BillPayment field', 'customer'), on_delete=models.SET_NULL)
    room = models.ForeignKey(
        Room, blank=True, null=True, related_name='billpayment_rooms',
        verbose_name=pgettext_lazy('BillPayment field', 'room'), on_delete=models.SET_NULL)
    amount = models.DecimalField(
        pgettext_lazy('BillPayment field', 'tax of the bill based on the amount'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    tax = models.DecimalField(
        pgettext_lazy('BillPayment field', 'tax of the bill based on the amount'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    date_paid = models.CharField(
        pgettext_lazy('BillPayment field', 'date_paid'), null=True, max_length=36)
    total_bills_amount_paid = models.DecimalField(
        pgettext_lazy('BillPaymentOption field', 'amount of the bill option'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    total_bills_amount = models.DecimalField(
        pgettext_lazy('BillPaymentOption field', 'amount of the bill option'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    total_bills_balance = models.DecimalField(
        pgettext_lazy('BillPaymentOption field', 'amount of the bill option'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    bill_paymentoption_map_id = models.CharField(
        pgettext_lazy('BillPayment field', 'id to map to bill payment options'), 
        null=True, max_length=200)
    deposit_refunded = models.BooleanField(
        pgettext_lazy('BillPayment field', 'is refunded'), default=True)
    updated_at = models.DateTimeField(
        pgettext_lazy('BillPayment field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('BillPayment field', 'created'),
                                   default=now, editable=False)
    objects = BillPaymentManager()

    class Meta:
        app_label = 'billpayment'
        verbose_name = pgettext_lazy('BillPayment model', 'BillPayment')
        verbose_name_plural = pgettext_lazy('BillPayments model', 'BillPayments')

    def __str__(self):
        return self.invoice_number


class BillPaymentOption(models.Model):
    ''' invoice_number for generating invoices of that bill '''
    transaction_number = models.CharField(
        pgettext_lazy('BillPaymentOption field', 'transaction_number'), null=True, max_length=36)
    payment_option = models.ForeignKey(
        PaymentOptions, blank=True, null=True, related_name='bill_paymentoption',
        verbose_name=pgettext_lazy('BillPaymentOption field', 'payment_option'), on_delete=models.SET_NULL)
    tendered = models.DecimalField(
        pgettext_lazy('BillPaymentOption field', 'amount of the bill option'), max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    bill_paymentoption_map_id = models.CharField(
        pgettext_lazy('BillPaymentOption field', 'id to map to bill payment options'), null=True, max_length=200)

    updated_at = models.DateTimeField(
        pgettext_lazy('BillPaymentOption field', 'updated at'), auto_now=True, null=True)
    created = models.DateTimeField(pgettext_lazy('BillPaymentOption field', 'created'),
                                   default=now, editable=False)

    class Meta:
        app_label = 'billpayment'
        verbose_name = pgettext_lazy('BillPaymentOption model', 'BillPaymentOption')
        verbose_name_plural = pgettext_lazy('BillPaymentOptions model', 'BillPaymentOptions')

    def __str__(self):
        return self.transaction_number





