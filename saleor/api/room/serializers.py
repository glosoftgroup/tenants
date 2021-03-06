# booking rest api serializers

from rest_framework import serializers
from django.utils.formats import localize
from django.contrib.auth import get_user_model
from saleor.booking.models import Book
from saleor.room.models import Maintenance as Table
from rest_framework.reverse import reverse

User = get_user_model()

class MaintenanceListSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()
    date_resolved = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    date_resolved = serializers.SerializerMethodField()
    paid_by = serializers.SerializerMethodField()

    invoice_url = serializers.HyperlinkedIdentityField(view_name='dashboard:fix-issue-invoice')
    issue_url = serializers.SerializerMethodField()
    delete_url = serializers.HyperlinkedIdentityField(view_name='dashboard:delete-issue')
    fix_issue_url = serializers.HyperlinkedIdentityField(view_name='dashboard:fix-issue')
    orders_url = serializers.HyperlinkedIdentityField(view_name='order-api:api-room-orders')

    class Meta:
        model = Table
        fields = (
                  'id',
                  'issue',
                  'date_reported',
                  'date_resolved',
                  'cost',
                  'amount_paid',
                  'balance',
                  'is_fixed',
                  'paid_by',
                  'room',
                  'created',
                  'updated_at',
                  'invoice_url',
                  'issue_url',
                  'delete_url',
                  'fix_issue_url',
                  'orders_url'
                 )
        # lookup_field = 'room__pk'

    def get_room(self, obj):
        details = None
        try:
          details = ({"id":obj.room.id, "name":obj.room.name, "wing":"Left Wing"})
        except:
          details = None

        return details
    def get_date_resolved(self, obj):
        resolved = "..."
        if obj.date_resolved:
            resolved = obj.date_resolved
        return resolved

    def get_cost(self, obj):
        return "{:,}".format(obj.cost.gross)

    def get_balance(self, obj):
        return "{:,}".format(obj.balance.gross)

    def get_amount_paid(self, obj):
        return "{:,}".format(obj.amount_paid.gross)

    def get_issue_url(self, obj):
        return reverse('dashboard:add_room_issue', kwargs={'pk': obj.room.pk})

    def get_paid_by(self, obj):
        customer = obj.paid_by
        if obj.paid_by == 'tenant':
            try:
                book = Book.objects.get(room__pk=obj.room.pk, active=True)
                customer = book.customer.name
            except:
                customer = obj.paid_by

        return customer