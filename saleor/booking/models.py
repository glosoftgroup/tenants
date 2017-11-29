from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import pgettext_lazy
from ..room.models import Room
from ..customer.models import Customer


class Book(models.Model):
    name = models.CharField(
        pgettext_lazy('Book field', 'Table name'),
        max_length=52, )
    orders = models.IntegerField(default=Decimal(0))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='booking_user',
        verbose_name=pgettext_lazy('Book field', 'user'))
    customer = models.ForeignKey(
        Customer, blank=True, null=True, related_name='booking_customers',
        verbose_name=pgettext_lazy('Book field', 'customer'))
    room = models.ManyToManyField(
        Room, verbose_name=pgettext_lazy('Book field', 'rooms'),
        related_name='booking_room')
    date_from = models.DateTimeField(
        pgettext_lazy('Book field', 'Date from'),
        default=now, editable=False)
    date_until = models.DateTimeField(
        pgettext_lazy('Book field', 'Date until'),
        default=now, editable=False)
    created = models.DateTimeField(
        pgettext_lazy('Book field', 'created'),
        default=now, editable=False)

    class Meta:
        verbose_name = pgettext_lazy('Booking model', 'Booking')
        verbose_name_plural = pgettext_lazy('Booking model', 'Bookings')

    def __str__(self):
        return str(self.name) + ' #' + str(self.number)

