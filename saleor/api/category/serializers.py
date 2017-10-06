# table rest api serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...product.models import Category
from rest_framework.serializers import (
                HyperlinkedIdentityField,
                )
User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    product_variants_url = HyperlinkedIdentityField(view_name='variant-api:api-variant-list')

    class Meta:
        model = Category
        fields = ('id',
                 'name',
                 'description',
                 'product_variants_url')