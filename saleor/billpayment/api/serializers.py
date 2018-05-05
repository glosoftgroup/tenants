# site settings rest api serializers

from rest_framework import serializers
from saleor.billpayment.models import BillPayment as Table
from saleor.billpayment.models import BillPaymentOption
from saleor.paymentoptions.models import PaymentOptions
from saleor.bill.models import Bill
import random

global fields, module
module = 'billpayment'
fields = ('id',
          'date_paid')


class TableListSerializer(serializers.ModelSerializer):
    invoice_url = serializers.HyperlinkedIdentityField(view_name=module + ':invoice')
    update_url = serializers.HyperlinkedIdentityField(view_name=module+':api-update')
    delete_url = serializers.HyperlinkedIdentityField(view_name=module+':api-delete')
    customer = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    bill = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = fields + (
            'invoice_number',
            'customer', 'room',
            'bill', 'tax', 'tax_is_filed', 'amount', 'income', 'date_paid',
            'total_bills_amount',
            'total_bills_amount_paid',
            'total_bills_balance', 'invoice_url',
            'update_url', 'delete_url',)

    def get_bill(self, obj):
        try:
            return {
                "id":obj.bill.id, 
                "name":obj.bill.billtype.name, 
                "amount":obj.bill.amount,
                "month":obj.bill.month.strftime('%B, %Y')
                }
        except Exception as e:
            print (e)
            return 'Not Set'

    def get_customer(self, obj):
        try:
            return {"id":obj.customer.id, "name":obj.customer.name}
        except:
            return 'Not Set'

    def get_room(self, obj):
        try:
            return {"id":obj.room.id, "name":obj.room.name}
        except:
            return 'Not Set'

    def get_income(self, obj):
        try:
            return (obj.amount - obj.tax)
        except:
            return 'Not Computed'

class BillOptionsListSerializer(serializers.ModelSerializer):
    payment_option = serializers.SerializerMethodField()

    class Meta:
        model = BillPaymentOption
        fields = ('id', 'transaction_number', 'tendered','bill_paymentoption_map_id','payment_option')

    def get_payment_option(self, obj):
        try:
            return {"id":obj.payment_option.id, "name":obj.payment_option.name}
        except:
            return ''


class CreateListSerializer(serializers.ModelSerializer):
    bills = serializers.JSONField(write_only=True)
    paymentoptions = serializers.JSONField(write_only=True)

    class Meta:
        model = Table
        fields = fields + (
            'bills','paymentoptions','date_paid',
            'total_bills_amount',
            'total_bills_balance',
            'total_bills_amount_paid',)

    def create(self, validated_data):
        ins = Table()
        bill_paymentoption_map_id = 'inv/bk/1' + ''.join(random.choice('0123456789ABCDEF') for i in range(4))
        ''' loop through the bills adding each '''
        for i in validated_data.get('bills'):
            instance = Table()
            ''' create the invoice number '''
            try:
                invoice_number = 'inv/bk/0' + str(Table.objects.latest('id').id)
                invoice_number += ''.join(random.choice('0123456789ABCDEF') for i in range(4))
            except Exception as e:
                invoice_number = 'inv/bk/1' + ''.join(random.choice('0123456789ABCDEF') for i in range(4))

            ''' get the bill '''
            try:
                bill = Bill.objects.get(pk=i['id'])
            except Exception as e:
                bill = None

            instance.invoice_number = invoice_number
            instance.amount = bill.amount
            instance.tax = bill.tax
            instance.customer = bill.customer
            instance.room = bill.room
            instance.bill = bill
            instance.date_paid = validated_data.get('date_paid')
            instance.bill_paymentoption_map_id = bill_paymentoption_map_id
            instance.total_bills_balance = validated_data.get('total_bills_balance')
            instance.total_bills_amount = validated_data.get('total_bills_amount')
            instance.total_bills_amount_paid = validated_data.get('total_bills_amount_paid')
            bill.status = 'fully-paid'
            bill.save()
            instance.save()

        for i in validated_data.get('paymentoptions'):
            try:
                option = PaymentOptions.objects.get(pk=i['id'])
            except Exception as e:
                option = None
            paymentOption = BillPaymentOption()
            paymentOption.tendered = i['tendered']
            try:
                paymentOption.transaction_number = i['transaction_number']
            except:
                paymentOption.transaction_number = ''
            paymentOption.payment_option = option
            paymentOption.bill_paymentoption_map_id = bill_paymentoption_map_id
            paymentOption.save()

        return ins


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
