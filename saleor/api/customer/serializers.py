from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import (
                    SerializerMethodField,
                    ValidationError,
                 )

from django.contrib.auth import get_user_model
User = get_user_model()
from ...customer.models import Customer
from ...booking.models import RentPayment
from ...sale.models import PaymentOption
from ...utils import image64
from rest_framework.reverse import reverse


class CustomerListSerializer(serializers.ModelSerializer):    
    cash_equivalency = SerializerMethodField()
    edit_url = serializers.HyperlinkedIdentityField(view_name='dashboard:customer-edit')
    sales_url = serializers.HyperlinkedIdentityField(view_name='dashboard:customer-sales-detail')
    detail_url = serializers.HyperlinkedIdentityField(view_name='dashboard:customer-detail')
    delete_url = serializers.HyperlinkedIdentityField(view_name='dashboard:customer-delete')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
                 'id',
                 'name',
                 'email',                 
                 'mobile',
                 'image',
                 'sales_url',
                 'delete_url',
                 'edit_url',
                 'detail_url',
                 'loyalty_points',
                 'redeemed_loyalty_points',
                 'cash_equivalency'
                 )

    def get_image(self, obj):
        image = ''
        if obj.image:
            image = obj.image.url
        else:
            image = image64()
        return image

    def get_cash_equivalency(self, obj):
        points_eq = PaymentOption.objects.filter(name='Loyalty Points')
        if not points_eq.exists():
            points_eq = 0
        else:
            points_eq = points_eq.get().loyalty_point_equiv
        if points_eq != 0:
                return obj.loyalty_points/Decimal(points_eq)
        return 0


class CreditWorthyCustomerSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Customer
        fields = (
                 'id',
                 'name',
                 'mobile')


class CustomerUpdateSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Customer
        fields = (
                 'id',
                 'name',
                 'email',                 
                 'mobile',
                 'loyalty_points',                 
                 )

    def validate_loyalty_points(self,value):        
        data = self.get_initial()
        self.points = data.get('loyalty_points')
        try:
            print Decimal(self.points)
        except:
            raise ValidationError('Invalid loyalty points')
    
    def update(self, instance, validated_data):   	
        instance.loyalty_points -= Decimal(self.points)
        instance.redeemed_loyalty_points += Decimal(self.points)
        instance.save()
        return instance

class PaymentListSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    total_balance = serializers.SerializerMethodField()
    maintenance_charges = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    payment_detail = serializers.SerializerMethodField()

    class Meta:
        model = RentPayment
        fields = ('id',
                  'invoice_number',
                  'customer',
                  'total_amount',
                  'amount_paid',
                  'maintenance_charges',
                  'balance',
                  'total_balance',
                  'date_paid',
                  'customer',
                  'room',
                  'description',
                  'created',
                  'payment_detail'
                 )

    def get_total_amount(self, obj):
        try:
            return obj.total_amount.gross
        except Exception as e:
            return 0

    def get_amount_paid(self, obj):
        try:
            return obj.amount_paid.gross
        except Exception as e:
            return 0

    def get_balance(self, obj):
        try:
            return obj.balance.gross
        except Exception as e:
            return 0

    def get_total_balance(self, obj):
        try:
            return obj.total_balance.gross
        except Exception as e:
            return 0

    def get_maintenance_charges(self, obj):
        try:
            return obj.maintenance_charges.gross
        except Exception as e:
            return 0

    def get_customer(self, obj):
        try:
            return {"id":obj.customer.id, "name":obj.customer.name}
        except Exception as e:
            print e
            return 'None Set'

    def get_room(self, obj):
        try:
            return {"id":obj.room.id, "name":obj.room.name}
        except Exception as e:
            print e
            return 'None Set'

    def get_payment_detail(self, obj):
        return reverse('dashboard:customer-detail', kwargs={'pk': obj.customer.pk})
