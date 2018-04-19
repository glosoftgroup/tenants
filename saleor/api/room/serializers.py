# booking rest api serializers

from rest_framework import serializers
from django.utils.formats import localize
from django.contrib.auth import get_user_model
from saleor.booking.models import Book
from saleor.room.models import Maintenance as Table
# from django.urls import reverse
from rest_framework.reverse import reverse

User = get_user_model()


class RoomHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'dashboard:add_room_issue'
    queryset = Table.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'room_pk': obj.room.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'pk': view_kwargs['room_pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


class MaintenanceListSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()
    date_resolved = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    date_resolved = serializers.SerializerMethodField()

    invoice_url = serializers.HyperlinkedIdentityField(view_name='dashboard:fix-issue-invoice')
    # issue_url = serializers.HyperlinkedIdentityField(view_name='dashboard:add_room_issue', read_only=True,
    #     lookup_url_kwarg={'room__pk':''})
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
                  'is_chargeable',
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