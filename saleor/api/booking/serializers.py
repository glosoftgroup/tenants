# booking rest api serializers

from django.db.models import Q
from rest_framework import serializers
from django.utils.formats import localize
from django.contrib.auth import get_user_model
from saleor.booking.models import Book as Table
from ...orders.models import Orders
from saleor.booking.models import Payment
from saleor.customer.models import Customer
from saleor.billtypes.models import BillTypes
from saleor.bill.models import Bill
from saleor.deposit.models import Deposit
import random
import datetime
import calendar
from decimal import Decimal

User = get_user_model()

global fields, module
module = 'bill'
fields = ('id',
          'active',
          'invoice_number',
          'total_rent',
          'total_service',
          'total_deposit',
          'deposit_months',
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
    total_booking_amount = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    bill_pending = serializers.SerializerMethodField()
    booking_edit = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-edit')
    booking_delete = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-delete')
    booking_detail = serializers.HyperlinkedIdentityField(view_name='dashboard:booking-detail')


    class Meta:
        model = Table
        fields = fields + (
            'booking_edit', 'booking_delete', 'date_in', 'date_out', 'bill_pending',
            'booking_detail', 'room_name', 'room_id', 'total_booking_amount')

    def get_bill_pending(self, obj):
        return Bill.objects.customer_bills(obj.customer, status='pending', billtype=None, booking=obj)

    def get_total_booking_amount(self, obj):
        try:
            return Decimal(obj.total_booking_amount())
        except Exception as e:
            print e
            return 0

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


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def bill_exist(month, customer, room, booking, billtype):
    """
    check if bill exist
    :param month: duration of lease
    :param customer: tenant object
    :param room: room object
    :param booking: booking model object
    :return: bool True if billing exist otherwise False
    """
    bills = Bill.objects.filter(
        Q(month=month) &
        Q(customer=customer) &
        Q(booking=booking) &
        Q(billtype=billtype) &
        Q(room=room)
    )
    if bills.exists():
        return True
    return False


def create_bill(instance, room, customer, months, check_in, deposit=0, update_deposit=0, check_out=''):
    """
    Create bills: deposits, rent and service types
    :param instance: object booking object
    :param room: object room(property) object
    :param customer: object customer(tenant) object
    :param months: int period of lease
    :param check_in: date lease should start
    :param deposit: Decimal amount to be paid for deposit
    :param update_deposit: Decimal (NOTE: when updating booking only) amount to be paid for deposit
    :param check_out: date (NOTE: when updating booking only) checkout date
    :return: VOID
    """
    # fetch bill types
    rent_type = BillTypes.objects.get(name="Rent")
    service_type = BillTypes.objects.get(name="Service")
    deposit_type = BillTypes.objects.get(name="Deposit")

    # fetch bills rent bills
    booking_list = Bill.objects.filter(booking=instance, room=room, customer=customer)

    # update deposit bill
    if update_deposit:
        update_deposit_instance = booking_list.filter(billtype=deposit_type)
        if update_deposit_instance.first():
            # update
            update_deposit_instance = update_deposit_instance.first()
            update_deposit_instance.customer = customer
            update_deposit_instance.amount = update_deposit
            update_deposit_instance.room = room
            update_deposit_instance.month = check_in
            update_deposit_instance.invoice_number = instance.invoice_number
            update_deposit_instance.save()
    # delete rent/service bills with months < or > check in date
    temp_check_in = add_months(check_in, 1)

    booking_list.filter(month__lte=temp_check_in, billtype=rent_type).delete()
    booking_list.filter(month__lte=temp_check_in, billtype=service_type).delete()

    booking_list.filter(month__gte=check_out, billtype=rent_type).delete()
    booking_list.filter(month__gte=check_out, billtype=service_type).delete()

    # tax calculation
    try:
        rent_tax = (room.price.gross * rent_type.tax) / 100
        service_tax = (room.service_charges * service_type.tax) / 100
    except Exception as e:
        print(e)

    if deposit != 0:
        print deposit
        deposit_type = BillTypes.objects.get(name="Deposit")
        Bill.objects.create(
                month=check_in, customer=customer,
                room=room, booking=instance,
                amount=deposit, billtype=deposit_type,
                invoice_number=instance.invoice_number)

    checker = 0
    for i in range(months):
        # rent
        bill = Bill()
        bill.month = add_months(check_in, checker)
        bill.customer = customer
        bill.invoice_number = instance.invoice_number
        bill.billtype = rent_type
        bill.room = room
        bill.amount = room.price.gross
        bill.booking = instance
        bill.tax = rent_tax
        bill.is_taxable = True
        # check if bill exist before saving
        exist = bill_exist(bill.month, bill.customer, bill.room, bill.booking, bill.billtype)
        if not exist:
            bill.save()

        # service
        bill.pk = None
        bill.amount = room.service_charges
        bill.billtype = service_type
        bill.tax = service_tax
        bill.is_taxable = True
        if not exist:
            bill.save()

        check_in = bill.month
        checker = 1


class CreateListSerializer(serializers.ModelSerializer):
    room_service_price = serializers.SerializerMethodField()
    room_rent_price = serializers.SerializerMethodField()
    last_payment = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = fields + ('room_service_price', 'room_rent_price', 'last_payment')

    def validate_total_rent(self, value):
        data = self.get_initial()
        try:
            value = Decimal(data.get('total_rent'))
        except:
            raise serializers.ValidationError('Total rent should be a decimal/integer')

        return value

    def get_last_payment(self, obj):
        try:
            detail = []
            payment = obj.bill_booking.filter(status='fully-paid')
            deposit_payment = payment.filter(billtype__name='Rent').order_by('month').first()
            payment = payment.order_by('month').first()
            detail.append({
                'month': payment.month,
                'billtype': payment.billtype.name,
                'amount': payment.amount,
                'days': obj.days,
                'deposit': deposit_payment.amount
            })

            return detail
        except Exception as e:
            print(e)
            return ''

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

        # mark room as booked
        room = validated_data.get('room')
        room.is_booked = True
        room.save()

        instance = Table.objects.create(**validated_data)
        # mark book as active
        instance.active = True
        instance.save()

        deposit = validated_data.get('total_deposit')

        # create bills
        months = validated_data.get('days')
        check_in = validated_data.get('check_in')

        create_bill(instance, room, customer, months, check_in, deposit)

        return instance

    def update(self, instance, validated_data):
        # update bill
        months = validated_data.get('days', instance.days)
        check_in = validated_data.get('check_in', instance.check_in)
        check_out = validated_data.get('check_out', instance.check_out)
        update_deposit = validated_data.get('total_deposit', instance.check_out)
        room = validated_data.get('room', instance.room)
        try:
            customer = validated_data['customer']
        except:
            customer = Customer.objects.get(mobile=validated_data['customer_mobile'])
            validated_data['customer'] = customer

        # recreate bills
        create_bill(
            instance, room, customer, months, check_in, deposit=0,
            update_deposit=update_deposit, check_out=check_out
        )

        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.total_rent = validated_data.get('total_rent', instance.total_rent)
        instance.total_service = validated_data.get('total_service', instance.total_service)
        instance.days = validated_data.get('days', instance.days)
        instance.total_deposit = validated_data.get('total_deposit', instance.total_deposit)
        instance.deposit_months = validated_data.get('deposit_months', instance.deposit_months)
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


class CheckOutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def update(self, instance, validated_data):
        instance.active = False
        room = instance.room
        room.is_booked = False
        room.save()
        instance.save()

        return instance
