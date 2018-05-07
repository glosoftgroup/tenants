from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import pagination
from .pagination import PostLimitOffsetPagination

from saleor.billpayment.models import BillPayment as Table
from saleor.billpayment.models import BillPaymentOption
from .serializers import (
    CreateListSerializer,
    TableListSerializer,
    UpdateSerializer,
    BillOptionsListSerializer
     )

User = get_user_model()


class CreateAPIView(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = CreateListSerializer


class DestroyView(generics.DestroyAPIView):
    queryset = Table.objects.all()


class ListAPIView(generics.ListAPIView):
    """
        list details
        GET /api/setting/
    """
    serializer_class = TableListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PostLimitOffsetPagination

    def get_serializer_context(self):
        if self.request.GET.get('date'):
            return {"date": self.request.GET.get('date'), 'request': self.request}
        return {"date": None, 'request': self.request}

    def get_queryset(self, *args, **kwargs):
        try:
            if self.kwargs['pk']:
                queryset_list = Table.objects.filter(customer__pk=self.kwargs['pk'])
            else:
                queryset_list = Table.objects.all()
            print ('pk is '+str(self.kwargs['pk']))
        except Exception as e:
            print ('errr')*100
            print e
            queryset_list = Table.objects.all()

        try:
            if self.kwargs['rmpk']:
                queryset_list = queryset_list.filter(
                    Q(room__pk=self.kwargs['rmpk']) &
                    (Q(bill__billtype__name__icontains='Rent') |
                     Q(bill__billtype__name__icontains="Maintenance")))
            else:
                queryset_list = queryset_list
            print ('rmpk is ' + str(self.kwargs['rmpk']))
        except Exception as e:
            print e
            # queryset_list = Table.objects.all()
            pass

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(page_size)
        else:
            pagination.PageNumberPagination.page_size = 10
        if self.request.GET.get('date'):
            queryset_list = queryset_list.filter(date_paid__icontains=self.request.GET.get('date'))
        if self.request.GET.get('month'):
            queryset_list = queryset_list.filter(
                bill__month__icontains=self.request.GET.get('month')
                )

        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(invoice_number__icontains=query)|
                Q(bill__billtype__name__icontains=query)|
                Q(customer__name__icontains=query)|
                Q(room__name__icontains=query))
        return queryset_list.order_by('-id')


class UpdateAPIView(generics.RetrieveUpdateAPIView):
    """
        update instance details
        @:param pk house id
        @:method PUT

        PUT /api/house/update/
        payload Json: /payload/update.json
    """
    queryset = Table.objects.all()
    serializer_class = UpdateSerializer


class OptionsListAPIView(generics.ListAPIView):
    serializer_class = BillOptionsListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PostLimitOffsetPagination

    def get_serializer_context(self):
        if self.request.GET.get('date'):
            return {"date": self.request.GET.get('date'), 'request': self.request}
        return {"date": None, 'request': self.request}

    def get_queryset(self, *args, **kwargs):
        return BillPaymentOption.objects.all().order_by('-id')
        
