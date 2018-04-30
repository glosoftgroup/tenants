# booking rest api serializers

from rest_framework import serializers
from django.utils.formats import localize
from django.contrib.auth import get_user_model
from saleor.booking.models import Book as Table
from ...orders.models import Orders
from saleor.booking.models import Payment
from saleor.customer.models import Customer
import random
from decimal import Decimal

User = get_user_model()

global fields, module
module = 'bill'
fields = ('id',
          'active',
          'invoice_number',
          'total_rent',
          'total_service',
          'days',
          'child',
          'adult',
          'check_in',
          'check_out',
          'customer',
          'customer_name',
          'customer_mobile',
          'room',
          'description',
          'user',)


class BookingListSerializer(serializers.ModelSerializer):
    total_rent = serializers.SerializerMethodField()
    total_service = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()
    date_in = serializers.SerializerMethodField()
    date_out = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    booking_edit = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-edit')
    booking_delete = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-delete')
    booking_detail = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-detail')

    class Meta:
        model = Table
        fields = fields + (
            'booking_edit', 'booking_delete', 'date_in', 'date_out',
            'booking_detail', 'room_name', 'room_id')

    def get_total_rent(self, obj):
        try:
            return "{:,}".format(obj.total_rent)
        except:
            return 0

    def get_total_service(self, obj):
        try:
            return "{:,}".format(obj.total_service)
        except:
            return 0


    def get_room_name(self, obj):
        try:
            return obj.room.name
        except:
            return ''

    def get_room_id(self, obj):
        try:
            return obj.room.pk
        except:
             return ''

    def get_customer_name(self, obj):
        return obj.customer.name

    def get_date_in(self, obj):
        return localize(obj.check_in)

    def get_date_out(self, obj):
        return localize(obj.check_out)

    def get_new_orders(self, obj):
        return len(Orders.objects.get_room_new_orders(obj.room_id))


class PaymentListSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id',
                  'invoice_number',
                  'book',
                  'amount',
                  'payment_option',
                  'date',
                  'customer_name',
                  'description',
                  'created'
                 )

    def get_amount(self, obj):
        try:
            return obj.amount_paid.gross
        except Exception as e:
            return 0

    def get_customer_name(self, obj):
        try:
            return obj.customer.name
        except Exception as e:
            print e
            return ''


class CreateListSerializer(serializers.ModelSerializer):
    # total_rent = serializers.SerializerMethodField()
    # total_service = serializers.SerializerMethodField()
    room_service_price = serializers.SerializerMethodField()
    room_rent_price = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = fields + ('room_service_price', 'room_rent_price')

    def validate_total_rent(self, value):
        data = self.get_initial()
        try:
            value = Decimal(data.get('total_rent'))
        except:
            raise serializers.ValidationError('Total rent should be a decimal/integer')

        return value

    def get_room_service_price(self, obj):
        return obj.room.service_charges

    def get_room_rent_price(self, obj):
        return obj.room.price.gross

    def get_total_rent(self, obj):
        return "{:,}".format(obj.total_rent)

    def get_total_service(self, obj):
        return "{:,}".format(obj.total_service)

    def create(self, validated_data):
        try:
            invoice_number = 'inv/bk/0' + str(Table.objects.latest('id').id)
            invoice_number += ''.join(random.choice('0123456789ABCDEF') for i in range(4))
        except Exception as e:
            invoice_number = 'inv/bk/1' + ''.join(random.choice('0123456789ABCDEF') for i in range(4))

        validated_data['invoice_number'] = invoice_number

        try:
            customer = validated_data['customer']
        except:
            customer = Customer()
            customer.name = validated_data['customer_name']
            customer.mobile = validated_data['customer_mobile']
            customer.save()
            validated_data['customer'] = customer
        room = validated_data.get('room')
        room.is_booked = True
        room.save()
        instance = Table.objects.create(**validated_data)
        # Table.objects.all().delete()
        return instance

    def update(self, instance, validated_data):
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.total_rent = validated_data.get('total_rent', instance.total_rent)
        instance.total_service = validated_data.get('total_service', instance.total_service)
        instance.days = validated_data.get('days', instance.days)
        instance.child = validated_data.get('child', instance.child)
        instance.adult = validated_data.get('adult', instance.adult)
        instance.check_in = validated_data.get('check_in', instance.check_in)
        instance.check_out = validated_data.get('check_out', instance.check_out)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_mobile = validated_data.get('customer_mobile', instance.customer_mobile)
        instance.room = validated_data.get('room', instance.room)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
