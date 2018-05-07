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
    tax = serializers.CharField(source='amount', read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ('period', 'tax', 'detail_url')

    def get_detail_url(self, obj):
        url = "%s?year=%s" % (reverse('billpayment:tax-detail'), self.context['current_year'])

        if self.context['request'].GET.get('month_from') and self.context['request'].GET.get('month_to'):
            month_from = self.context['request'].GET.get('month_from')
            month_to = self.context['request'].GET.get('month_to')
            url = "%s?month_from=%s&month_to=%s" % (reverse('billpayment:tax-detail'), month_from, month_to)

        if self.context['request'].GET.get('month') and self.context['request'].GET.get('year'):
            month = self.context['request'].GET.get('month')
            year = self.context['request'].GET.get('year')
            url = "%s?month=%s&year=%s" % (reverse('billpayment:tax-detail'), month, year)

        return url
