# site settings rest api serializers

from rest_framework import serializers
from saleor.bill.models import Bill as Table
from saleor.booking.models import Book
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
import random

global fields, module
module = 'bill'
fields = ('id',
          'invoice_number',
          'customer',
          'booking',
          'room',
          'billtype',
          'amount',
          'tax',
          'is_taxable',
          'month',
          'status',
          'description')


class TableListSerializer(serializers.ModelSerializer):
    invoice_url = serializers.HyperlinkedIdentityField(view_name=module+':invoice')
    update_url = serializers.HyperlinkedIdentityField(view_name=module+':update')
    payment_id = serializers.SerializerMethodField()
    delete_url = serializers.HyperlinkedIdentityField(view_name=module+':api-delete')
    customer = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    billtype = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    deposit_refunded = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = fields + ('month', 'deposit_refunded', 'invoice_url', 'payment_id', 'update_url', 'delete_url',)

    def get_deposit_refunded(self, obj):
        try:
            return obj.billpayment.get(bill=obj.id).deposit_refunded
        except Exception as e:
            print(e)
            return 0

    def get_payment_id(self, obj):
        try:
            return obj.billpayment.first().id
        except Exception as e:
            print(e)
            return 0

    def get_month(self, obj):
        try:
            return obj.month.strftime('%B %Y')
        except:
            return 'None Set'
            
    def get_customer(self, obj):
        try:
            return {"id":obj.customer.id, "name":obj.customer.name}
        except:
            return 'None Set'

    def get_billtype(self, obj):
        try:
            return {"id":obj.billtype.id, "name":obj.billtype.name}
        except:
            return 'None Set'

    def get_amount(self, obj):
        try:
            return obj.amount
        except:
            return '0'

    def get_room(self, obj):
        try:
            return {"id":obj.room.id, "name":obj.room.name}
        except:
            return 'Not Set'


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Table.objects.all(),
                fields=('customer', 'room', 'billtype', 'month'),
                message=_("Bill Setting Already Exists.")
            )
        ]

    def validate_amount(self, data):
        data = self.get_initial()
        try:
            value = Decimal(data.get('amount'))
        except:
            raise serializers.ValidationError('Bill Amount should be a decimal/integer')

        return value
    def validate_invoice_number(self, data):
        try:
            invoice_number = 'inv/bk/0' + str(Table.objects.latest('id').id)
            invoice_number += ''.join(random.choice('0123456789ABCDEF') for i in range(4))
        except Exception as e:
            invoice_number = 'inv/bk/1' + ''.join(random.choice('0123456789ABCDEF') for i in range(4))

        return invoice_number

    def create(self, validated_data):
        instance = Table.objects.create(**validated_data)
        instance.save()

        return instance


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def validate_amount(self, data):
        data = self.get_initial()
        try:
            value = Decimal(data.get('amount'))
        except:
            raise serializers.ValidationError('Bill Amount should be a decimal/integer')

        return value

    def validate_tax(self, data):
        data = self.get_initial()
        try:
            value = Decimal(data.get('tax'))
        except:
            raise serializers.ValidationError('Bill Amount should be a decimal/integer')

        return value

    def update(self, instance, validated_data):

        if not instance.invoice_number:
            try:
                invoice_number = 'inv/bk/0' + str(Table.objects.latest('id').id)
                invoice_number += ''.join(random.choice('0123456789ABCDEF') for i in range(4))
            except Exception as e:
                invoice_number = 'inv/bk/1' + ''.join(random.choice('0123456789ABCDEF') for i in range(4))
            instance.invoice_number = invoice_number

        instance.billtype = validated_data.get('billtype', instance.billtype)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.is_taxable = validated_data.get('is_taxable', instance.is_taxable)
        instance.tax = validated_data.get('tax', instance.tax)
        if instance.is_taxable == False:
            instance.tax = Decimal(0)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.room = validated_data.get('room', instance.room)
        instance.month = validated_data.get('month', instance.month)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class TenantsListSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('customer', 'room')

            
    def get_customer(self, obj):
        try:
            return {"id":obj.customer.id, "name":obj.customer.name}
        except:
            return 'None Set'

    def get_room(self, obj):
        try:
            return {"id":obj.room.id, "name":obj.room.name}
        except:
            return 'None Set'

