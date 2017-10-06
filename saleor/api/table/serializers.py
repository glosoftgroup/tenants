# table rest api serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...table.models import Table
User = get_user_model()


class TableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id',
                 'name',
                 )