# site settings rest api serializers

from rest_framework import serializers
from saleor.billpayment.models import BillPayment as Table
from saleor.billpayment.models import BillPaymentOption
from saleor.bill.models import Bill
import random

global fields, module
module = 'billpayment'
fields = ('id',
          'date_paid')


class TableListSerializer(serializers.ModelSerializer):
    update_url = serializers.HyperlinkedIdentityField(view_name=module+':api-update')
    delete_url = serializers.HyperlinkedIdentityField(view_name=module+':api-delete')
    text = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = fields + ('text', 'update_url', 'delete_url',)

    def get_text(self, obj):
        try:
            return obj.name
        except:
            return ''


class CreateListSerializer(serializers.ModelSerializer):
    bills = serializers.JSONField(write_only=True)
    paymentoptions = serializers.JSONField(write_only=True)
    class Meta:
        model = Table
        fields = fields + ('bills','paymentoptions', 'date_paid',)
        # fields = fields + ('bills',)

    def create(self, validated_data):
        ins = Table()
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
            # try:
            #     bill = Bill.objects.get(pk=i['id'])
            # except Exception as e:
            #     bill = None
            #     print (e)
            print ('-')*100
            print "invoice_number "+str(invoice_number)
            print "invoice_number "+str(invoice_number)
            print "bill customer "+str(i['customer']['id'])
            print "bill room "+str(i['room']['id'])
            print "date_paid "+str(validated_data.get('date_paid'))
            print ('*')*100
            print "bill id "+str(i['id'])
            print "tax "+str(i['tax'])
            print "amount "+str(i['amount'])
            print ('-')*100

            # instance.invoice_number = invoice_number
            # instance.amount = i['amount']
            # instance.tax = i['tax']
            # instance.customer = validated_data.get('customer')
            # instance.room = validated_data.get('room')
            # instance.bill = i['id']
            # instance.date_paid = validated_data.get('date_paid')

        for i in validated_data.get('paymentoptions'):
            print ('?')*100
            print "id "+str(i['id'])
            print "name "+str(i['name'])
            print "tendered "+str(i['tendered'])
            print "transaction_number "+str(i['transaction_number'])
            print ('?')*100


            # if 'assignment' in str(i['name'])



        # instance.save()

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
