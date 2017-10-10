from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from ...orders.models import Orders

from .serializers import (
    ListOrderSerializer,
    OrderSerializer,
     )

import logging
User = get_user_model()
debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):              
        serializer.save(user=self.request.user)      

        
class OrderListAPIView(generics.ListAPIView):
    serializer_class = ListOrderSerializer

    def get_queryset(self, *args, **kwargs):        
        queryset_list = Orders.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(invoice_number__icontains=query)               
                ).distinct()
        return queryset_list


class OrderStatusListAPIView(generics.ListAPIView):
    serializer_class = ListOrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Orders.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(status=query)
                ).distinct()
        return queryset_list


class SalePointOrdersListAPIView(generics.ListAPIView):
    serializer_class = ListOrderSerializer
    queryset = Orders.objects.all()

    def list(self, request, pk=None):
        # Note the use of `get_queryset()` instead of `self.queryset`
        query = self.request.GET.get('q')
        if query:
            queryset = self.get_queryset().filter(sale_point__pk=pk).filter(status=query)
        else:
            queryset = self.get_queryset().filter(sale_point__pk=pk)
        serializer = ListOrderSerializer(queryset, many=True)
        return Response(serializer.data)


class TableOrdersListAPIView(generics.ListAPIView):
    serializer_class = ListOrderSerializer
    queryset = Orders.objects.all()

    def list(self, request, pk=None):
        # Note the use of `get_queryset()` instead of `self.queryset`
        query = self.request.GET.get('q')
        if query:
            queryset = self.get_queryset().filter(table__pk=pk).filter(status=query)
        else:
            queryset = self.get_queryset().filter(table__pk=pk)
        serializer = ListOrderSerializer(queryset, many=True)
        return Response(serializer.data)