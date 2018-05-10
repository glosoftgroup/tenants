# site settings rest api serializers

from rest_framework import serializers
from saleor.billpayment.models import BillPayment as Table
from django.core.urlresolvers import reverse

global fields, module
module = 'billpayment'
fields = ('id',
          'date_paid')


class TableListSerializer(serializers.ModelSerializer):
    period = serializers.DateField(format="%B %Y", input_formats=None, source='month', read_only=True)
    type = serializers.CharField(source='bill__billtype__name', read_only=True)
    tax = serializers.CharField(source='total_tax', read_only=True)
    amount = serializers.CharField(source='total_amount', read_only=True)
    rent = serializers.CharField(source='rents', read_only=True)
    property = serializers.CharField(source='room__name', read_only=True)
    services = serializers.CharField(source='service', read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ('period', 'type', 'tax', 'services', 'rent', 'amount', 'property', 'detail_url')

    def get_detail_url(self, obj):
        if self.context['request'].GET.get('property'):
            search_query = self.context['request'].GET.get('property')
        else:
            search_query = ''

        url = "%s?year=%s&property=%s" % (reverse('billpayment:income-detail'), self.context['current_year'], search_query)

        if self.context['request'].GET.get('month_from') and self.context['request'].GET.get('month_to'):
            month_from = self.context['request'].GET.get('month_from')
            month_to = self.context['request'].GET.get('month_to')
            url = "%s?month_from=%s&month_to=%s&property=%s" % (reverse('billpayment:income-detail'), month_from, month_to, search_query)

        if self.context['request'].GET.get('month') and self.context['request'].GET.get('year'):
            month = self.context['request'].GET.get('month')
            year = self.context['request'].GET.get('year')
            url = "%s?month=%s&year=%s&property=%s" % (reverse('billpayment:income-detail'), month, year, search_query)

        return url
