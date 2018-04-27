# site settings rest api serializers

from rest_framework import serializers
from saleor.bill.models import Bill as Table

global fields, module
module = 'bill'
fields = ('id',
          'name',
          'description')


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
    class Meta:
        model = Table
        fields = fields

    def create(self, validated_data):
        instance = Table()
        instance.name = validated_data.get('name')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        instance.save()

        return instance


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = fields

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance
