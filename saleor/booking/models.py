from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.translation import pgettext_lazy
from django.core.validators import MinValueValidator, RegexValidator
from django_prices.models import PriceField
from ..room.models import Room
from saleor.sale.models import PaymentOption
from ..customer.models import Customer


class ModelManager(models.Manager):
    def monthly_visits_data(self, year=None):
        final_data = []
        last_instance = self.get_queryset().latest('id')
        if not year:
            year = DateFormat(last_instance.created).format('Y')
        for day in xrange(1, 30):
            count = self.get_queryset().filter(
                                models.Q(created__year=year) &
                                models.Q(created__day=day)).count()
            final_data.append(count)
        return final_data

    def yearly_visits_data(self, year=None):
        """
        :param year:
        :return: Total visits each month
        """
        final_data = []
        last_instance = self.get_queryset().latest('id')
        if not year:
            year = DateFormat(last_instance.created).format('Y')
        for month in range(1, 13):
            count = self.get_queryset().filter(created__year=year)\
                                       .filter(created__month=month).count()
            final_data.append([str(year)+str(1)+str(month), count])
        return final_data

    def yearly_amount_data(self, year=None):
        """
        :param year:
        :return: total amount received in each month
        """
        final_data = []
        last_instance = self.get_queryset().latest('id')
        if not year:
            year = DateFormat(last_instance.created).format('Y')
        for month in range(1, 13):
            amount = self.get_queryset().filter(created__year=year)\
                                       .filter(created__month=month) \
                                       .aggregate(models.Sum('price'))['price__sum']
            if not amount:
                amount = 0
            else:
                amount = amount.gross
            final_data.append([str(year)+str(1)+str(month), float(str(amount))])
        return final_data

    def total_bookings(self, date, amount=False):
        """
        :param date: filter by this date
        :param amount: if set return total amount
        :return: return total booking in that date
        """
        if amount:
            total = self.get_queryset() \
                .filter(created__icontains=DateFormat(date)
                        .format('Y-m-d')).aggregate(models.Sum('price'))['price__sum']
            if total:
                total = float(str(total.gross))
            else:
                total = 0
            return total

        return self.get_queryset()\
                   .filter(created__icontains=DateFormat(date)
                           .format('Y-m-d')).count()


class Book(models.Model):
    invoice_number = models.CharField(
        pgettext_lazy('Book invoice', 'invoice number'),
        max_length=152, unique=True, null=True)
    description = models.CharField(
        pgettext_lazy('Book field', 'description'),
        max_length=152, default='', null=True, blank=True)
    customer_name = models.CharField(
        pgettext_lazy('Book field', 'customer name'),
        max_length=152, default='', null=True, blank=True)
    customer_mobile = models.CharField(
        pgettext_lazy('Book field', 'customer mobile'),
        max_length=152, default='', null=True, blank=True)
    total_rent = models.DecimalField(
        pgettext_lazy('Book field', 'total rent amount'), default=Decimal(0), max_digits=19, decimal_places=5)

    total_service = models.DecimalField(
        pgettext_lazy('Book field', 'total service amount'), default=Decimal(0), max_digits=19, decimal_places=5)
    price = PriceField(
        pgettext_lazy('Book field', 'booking amount'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    total = PriceField(
        pgettext_lazy('Book field', 'total booking amount'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    amount_paid = PriceField(
        pgettext_lazy('Book field', 'paid'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    balance = PriceField(
        pgettext_lazy('Book field', 'balance'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    days = models.IntegerField(default=Decimal(1))
    deposit_months = models.IntegerField(default=Decimal(1))
    total_deposit = models.DecimalField(
        pgettext_lazy('Book field', 'total deposit amount'),
        default=Decimal(0), max_digits=19, decimal_places=2)

    child = models.IntegerField(default=Decimal(0))
    adult = models.IntegerField(default=Decimal(1))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='booking_user',
        verbose_name=pgettext_lazy('Book field', 'user'))
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='booking_customers',
        verbose_name=pgettext_lazy('Book field', 'customer'))
    room = models.ForeignKey(
        Room, verbose_name=pgettext_lazy('Book field', 'rooms'),
        related_name='booking_room',  blank=True, null=True,)
    check_in = models.DateField(
        pgettext_lazy('Book field', 'Date from'),
        default=now)
    check_out = models.DateField(
        pgettext_lazy('Book field', 'Date until'),
        default=now)
    active = models.BooleanField(
        pgettext_lazy('Book field', 'is booked'), default=True)
    created = models.DateTimeField(
        pgettext_lazy('Book field', 'created'),
        default=now, editable=False)
    service_charges = PriceField(
        pgettext_lazy('Book field', 'service charges(property service charges added)'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    maintenance_charges = PriceField(
        pgettext_lazy('Book field', 'maintenance charges(maintenance fee added)'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    balance_with_charges = PriceField(
        pgettext_lazy('Book field', 'balance with maintenance charges included'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)

    objects = ModelManager()

    class Meta:
        verbose_name = pgettext_lazy('Booking model', 'Booking')
        verbose_name_plural = pgettext_lazy('Booking model', 'Bookings')

    def __str__(self):
        return str(self.id) + ' #' + str(self.invoice_number)

    def total_booking_amount(self):
        return self.total_rent + self.total_deposit + self.total_service


class Payment(models.Model):
    invoice_number = models.CharField(
        pgettext_lazy('Payment invoice', 'invoice number'),
        max_length=152, default='', blank=True, null=True)
    description = models.CharField(
        pgettext_lazy('Payment field', 'description'),
        max_length=152, default='', null=True, blank=True)
    price_type = models.CharField(
        pgettext_lazy('Payment field', 'price type'),
        max_length=152, default='', null=True, blank=True)
    payment_option = models.ForeignKey(
        PaymentOption, related_name='booking_payment_option', blank=True, null=True, default='',
        on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Payment field', 'table'))
    amount_paid = PriceField(
        pgettext_lazy('Payment field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    customer = models.ForeignKey(
        Customer, related_name='booking_payment', blank=True, null=True, default='', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Payment field', 'table'))
    book = models.ForeignKey(
        Book, related_name='booking_payment', blank=True, null=True, default='', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Payment field', 'table'))
    date = models.DateField(
        pgettext_lazy('Payment field', 'Date from'),
        default=now)
    created = models.DateField(
        pgettext_lazy('Payment field', 'created'),
        default=now, editable=False)


class BookingHistory(models.Model):
    invoice_number = models.CharField(
        pgettext_lazy('BookingHistory field', 'invoice number'),
        max_length=152, default='', blank=True, null=True)
    price = PriceField(
        pgettext_lazy('Book field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    book = models.ForeignKey(
        Book, related_name='booking_history_payment', blank=True, null=True, default='', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('BookingHistory field', 'table'))
    room = models.ForeignKey(
        Room, verbose_name=pgettext_lazy('Book field', 'rooms'),
        related_name='booking_history_room', blank=True, null=True, on_delete=models.SET_NULL )
    customer = models.ForeignKey(
        Customer, blank=True, null=True, on_delete=models.SET_NULL, related_name='booking_history_customers',
        verbose_name=pgettext_lazy('Book field', 'customer'))
    check_in = models.DateTimeField(
        pgettext_lazy('BookingHistory field', 'Date from'),
        default=now)
    check_out = models.DateTimeField(
        pgettext_lazy('BookingHistory field', 'Date until'),
        default=now)
    created = models.DateField(
        pgettext_lazy('BookingHistory field', 'created'),
        default=now, editable=False)

class RentPayment(models.Model):
    date_paid = models.CharField(
        pgettext_lazy('Payment field', 'date paid'),
        max_length=152, default='', null=True, blank=True)
    created = models.DateField(
        pgettext_lazy('Payment field', 'created'),
        default=now, editable=False)
    invoice_number = models.CharField(
        pgettext_lazy('Payment invoice', 'invoice number'),
        max_length=152, default='', blank=True, null=True)
    price_type = models.CharField(
        pgettext_lazy('Payment field', 'price type'),
        max_length=152, default='', null=True, blank=True)
    total_amount = PriceField(
        pgettext_lazy('Payment field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    total_balance = PriceField(
        pgettext_lazy('Payment field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    amount_paid = PriceField(
        pgettext_lazy('Payment field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    balance = PriceField(
        pgettext_lazy('Book field', 'balance'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    maintenance_charges = PriceField(
        pgettext_lazy('Book field', 'service charges'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        validators=[MinValueValidator(0)], default=Decimal(0), decimal_places=2)
    customer = models.ForeignKey(
        Customer, related_name='tenant_payment', blank=True, null=True, default='', on_delete=models.CASCADE,
        verbose_name=pgettext_lazy('Customer field', 'customer'))
    room = models.ForeignKey(
        Room, related_name='room_payment', blank=True, null=True, default='', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Customer field', 'room'))
    book = models.ForeignKey(
        Book, related_name='book_payment', blank=True, null=True, default='', on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Customer field', 'book'))
    payment_name = models.CharField(
        pgettext_lazy('Payment field', 'payment name'),
        max_length=152, default='None', null=True, blank=True)
    transaction_number = models.CharField(
        pgettext_lazy('Payment field', 'transaction number'),
        max_length=152, default='None', null=True, blank=True)

    description = models.CharField(
        pgettext_lazy('Payment field', 'description'),
        max_length=152, default='', null=True, blank=True)
