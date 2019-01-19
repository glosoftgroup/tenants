from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import pagination
from .pagination import PostLimitOffsetPagination

from saleor.billpayment.models import BillPayment as Table
from .serializers import (
    TableListSerializer,
     )

User = get_user_model()
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import datetime
now = datetime.datetime.now()


class ListAPIView(generics.ListAPIView):
    """
        list details
        GET /api/setting/
    """
    serializer_class = TableListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PostLimitOffsetPagination

    def get_serializer_context(self):
        try:
            current_year = Table.objects.last().bill.month.year
        except:
            current_year = now.year
        return {"date": None, 'request': self.request, 'current_year':current_year}

    def list(self, request, *args, **kwargs):
        response = super(ListAPIView, self).list(request, args, kwargs)
        try:
            current_year = Table.objects.last().bill.month.year
        except:
            current_year = now.year

        if self.request.GET.get('property'):
            search_query = self.request.GET.get('property')
            query_set = Table.objects.filter(room__name__icontains=str(search_query))
            try:
                response.data['property'] = query_set.first().room.name
            except:
                response.data['property'] = self.request.GET.get('property')
        else:
            query_set = Table.objects.all()
            response.data['property'] = ''

        response.data['period'] = current_year

        queryset = query_set.\
            filter(bill__month__year=str(current_year)).\
            exclude(tax__exact='-1').annotate(month=TruncMonth('bill__month')).\
            values('month').annotate(total_amount=Sum('amount')).annotate(total_tax=Sum('tax')).values('month', 'total_amount', 'total_tax', 'room__name')

        totalTax = queryset.aggregate(Sum('total_tax'))["total_tax__sum"]
        response.data['totalTax'] = totalTax
        totalAmount = queryset.aggregate(Sum('total_amount'))["total_amount__sum"]
        response.data['totalAmount'] = totalAmount

        queryset_all = query_set.exclude(tax__exact='-1').\
            annotate(month=TruncMonth('bill__month'))\
            .values('month').annotate(total_amount=Sum('amount')).annotate(total_tax=Sum('tax')).values('month', 'total_amount', 'total_tax', 'room__name')

        if self.request.GET.get('month_from') and self.request.GET.get('month_to'):
            month_from = self.request.GET.get('month_from')
            month_to = self.request.GET.get('month_to')
            queryset = queryset_all.filter(bill__month__range=[str(month_from), str(month_to)])

            totalTax = queryset.aggregate(Sum('total_tax'))["total_tax__sum"]
            response.data['totalTax'] = totalTax
            totalAmount = queryset.aggregate(Sum('total_amount'))["total_amount__sum"]
            response.data['totalAmount'] = totalAmount


        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = self.request.GET.get('month')
            year = self.request.GET.get('year')
            queryset = queryset_all.filter(bill__month__month=str(month),
                                           bill__month__year=str(year))

            totalTax = queryset.aggregate(Sum('total_tax'))["total_tax__sum"]
            response.data['totalTax'] = totalTax
            totalAmount = queryset.aggregate(Sum('total_amount'))["total_amount__sum"]
            response.data['totalAmount'] = totalAmount

        if self.request.GET.get('year') and not self.request.GET.get('month'):
            year = self.request.GET.get('year')
            queryset = queryset_all.filter(bill__month__year=str(year))

            totalTax = queryset.aggregate(Sum('total_tax'))["total_tax__sum"]
            response.data['totalTax'] = totalTax
            totalAmount = queryset.aggregate(Sum('total_amount'))["total_amount__sum"]
            response.data['totalAmount'] = totalAmount

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(page_size)
        else:
            pagination.PageNumberPagination.page_size = 10

        if not totalTax:
            response.data['totalTax'] = '0.00'
        if not totalAmount:
            response.data['totalAmount'] = '0.00'

        return response

    def get_queryset(self, *args, **kwargs):
        # display the latest years tax data first
        try:
            current_year = Table.objects.last().bill.month.year
        except:
            current_year = now.year

        if self.request.GET.get('property'):
            search_query = self.request.GET.get('property')
            query_set = Table.objects.filter(room__name__icontains=str(search_query))
        else:
            query_set = Table.objects.all()

        current_year_queryset = query_set.\
            filter(bill__month__year=str(current_year)).\
            exclude(tax__exact='0').annotate(month=TruncMonth('bill__month')).\
            values('month').annotate(total_amount=Sum('amount')).\
            annotate(total_tax=Sum('tax')).\
            values('month', 'total_amount', 'total_tax', 'room__name')

        queryset_all = query_set.exclude(tax__exact='0').\
            annotate(month=TruncMonth('bill__month'))\
            .values('month').annotate(total_amount=Sum('amount')).\
            annotate(total_tax=Sum('tax')).\
            values('month', 'total_amount', 'total_tax', 'room__name')

        queryset = current_year_queryset

        if self.request.GET.get('month_from') and self.request.GET.get('month_to'):
            month_from = self.request.GET.get('month_from')
            month_to = self.request.GET.get('month_to')
            queryset = queryset_all.filter(bill__month__range=[str(month_from), str(month_to)])

        if self.request.GET.get('month') and self.request.GET.get('year'):
            month = self.request.GET.get('month')
            year = self.request.GET.get('year')
            queryset = queryset_all.filter(bill__month__month=str(month),
                                           bill__month__year=str(year))
        if self.request.GET.get('year') and not self.request.GET.get('month'):
            year = self.request.GET.get('year')
            queryset = queryset_all.filter(bill__month__year=str(year))

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(page_size)
        else:
            pagination.PageNumberPagination.page_size = 10

        finalqueryset = queryset.values('month', 'total_amount', 'total_tax', 'room__name', 'bill__billtype__name')

        for i in queryset:
            i['service'] = 0

            for j in finalqueryset:
                if j['room__name'] == i['room__name'] and j['bill__billtype__name'] == 'Service':
                    i['service'] += j['total_amount']

            i['rents'] = i['total_amount'] - i['service']

        return queryset
