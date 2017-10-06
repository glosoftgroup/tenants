from __future__ import unicode_literals

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import pgettext_lazy
from django_prices.models import PriceField

from ..userprofile.models import Address
from ..customer.models import Customer
from ..sale.models import Terminal

from . import OrderStatus


class Orders(models.Model):
    status = models.CharField(
        pgettext_lazy('Orders field', 'Invoice status'),
        max_length=32, choices=OrderStatus.CHOICES, default=OrderStatus.NEW)
    created = models.DateTimeField(
        pgettext_lazy('Orders field', 'created'),
        default=now, editable=False)    
    last_status_change = models.DateTimeField(
        pgettext_lazy('Orders field', 'last status change'),
        default=now, editable=False)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='orders_customers',
        verbose_name=pgettext_lazy('Orders field', 'customer'))

    mobile = models.CharField(max_length=20, blank=True, null=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='orders_users',
        verbose_name=pgettext_lazy('Orders field', 'user'))
    language_code = models.CharField(max_length=35, default=settings.LANGUAGE_CODE)
    user_email = models.EmailField(
        pgettext_lazy('Orders field', 'user email'),
        blank=True, default='', editable=False)
    terminal = models.ForeignKey(
        Terminal, related_name='terminal_orders',blank=True, default='',
        verbose_name=pgettext_lazy('Orders field', 'order'))
    invoice_number = models.CharField(
        pgettext_lazy('Orders field', 'invoice_number'), unique=True, null=True, max_length=36,)
    
    total_net = models.DecimalField(
        pgettext_lazy('Orders field', 'total net'), default=Decimal(0), max_digits=100, decimal_places=2)
    
    sub_total = models.DecimalField(
        pgettext_lazy('Orders field', 'sub total'), default=Decimal(0), max_digits=100, decimal_places=2)
    
    total_tax = models.DecimalField(
        pgettext_lazy('Orders field', 'total tax'), default=Decimal(0), max_digits=100, decimal_places=2)
    amount_paid = models.DecimalField(
        pgettext_lazy('Orders field', 'amount paid'), default=Decimal(0), max_digits=100, decimal_places=2)
    
    balance = models.DecimalField(
        pgettext_lazy('Orders field', 'balance'), default=Decimal(0), max_digits=100, decimal_places=2)
    
    discount_amount = PriceField(
        verbose_name=pgettext_lazy('Orders field', 'discount amount'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        blank=True, null=True)
    discount_name = models.CharField(
        verbose_name=pgettext_lazy('Orders field', 'discount name'),
        max_length=255, default='', blank=True)

    class Meta:
        ordering = ('-last_status_change',)
        verbose_name = pgettext_lazy('Orders model', 'Order')
        verbose_name_plural = pgettext_lazy('Orders model', 'Orders')
        
    def __str__(self):
        return self.invoice_number

    def __unicode__(self):
        return unicode(self.invoice_number)


class OrderedItem(models.Model):
    order = models.ForeignKey(Orders, related_name='ordered_items',on_delete=models.CASCADE)
    order = models.IntegerField(default=Decimal(1))
    sku = models.CharField(
        pgettext_lazy('OrderdItem field', 'SKU'), max_length=32)
    quantity = models.IntegerField(
        pgettext_lazy('OrderdItem field', 'quantity'),
        validators=[MinValueValidator(0)], default=Decimal(1))
    product_name = models.CharField(
        pgettext_lazy('OrderdItem field', 'product name'), max_length=128)
    total_cost = models.DecimalField(
        pgettext_lazy('OrderdItem field', 'total cost'), default=Decimal(0), max_digits=100, decimal_places=2)
    unit_cost = models.DecimalField(
        pgettext_lazy('OrderdItem field', 'unit cost'), default=Decimal(0), max_digits=100, decimal_places=2)
    product_category = models.CharField(
        pgettext_lazy('OrderdItem field', 'product_category'), max_length=128, null=True)
    discount = models.DecimalField(
        pgettext_lazy('OrderdItem field', 'discount'), default=Decimal(0), max_digits=100, decimal_places=2)
    tax = models.IntegerField(default=Decimal(0))

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.product_name)

    def __str__(self):
        return self.product_name

