# table rest api serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...salepoints.models import SalePoint
User = get_user_model()


class SalePointListSerializer(serializers.ModelSerializer):
    orders_url = serializers.HyperlinkedIdentityField(view_name='order-api:api-sale_point-orders')

    class Meta:
        model = SalePoint
        fields = ('id',
                  'name',
                  'orders_url'
                 )