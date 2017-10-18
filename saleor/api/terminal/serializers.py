# Payment rest api serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...sale.models import Terminal
User = get_user_model()


class TerminalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('id',
                  'terminal_name',
                  'terminal_number')