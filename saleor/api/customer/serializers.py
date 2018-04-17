from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import (
                    SerializerMethodField,
                    ValidationError,
                 )

from django.contrib.auth import get_user_model
User = get_user_model()
from ...customer.models import Customer
from ...sale.models import PaymentOption
from ...utils import image64


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