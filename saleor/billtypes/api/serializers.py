# site settings rest api serializers

from rest_framework import serializers
from saleor.billtypes.models import BillTypes as Table
from django.db import models
global fields, module
module = 'billtypes'
fields = ('id',
          'name',
          'tax',
          'description')


class TableListSerializer(serializers.ModelSerializer):
    update_url = serializers.HyperlinkedIdentityField(view_name=module+':api-update')
    delete_url = serializers.HyperlinkedIdentityField(view_name=module+':api-delete')
    class Meta:
        model = Table
        fields = fields + ('update_url', 'delete_url',)


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def create(self, validated_data):
        instance = Table.objects.create(**validated_data)
        instance.save()

        return instance


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def update(self, instance, validated_data):
        bill_types = ['Rent', 'Deposit', 'Service', 'Maintenance', 'Electricity', 'Water']
        if instance.name in bill_types and instance.name != validated_data.get('name'):
            raise serializers.ValidationError('You cannot update ' + instance.name)
        instance.name = validated_data.get('name', instance.name)
        instance.tax = validated_data.get('tax', instance.tax)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
