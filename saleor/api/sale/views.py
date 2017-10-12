from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from ...orders.models import Orders
from ...sale.models import (
                            Sales,
                            SoldItem,
                            Terminal,
                            TerminalHistoryEntry,
                            DrawerCash
                            )

from .serializers import (
    ListSaleSerializer,
    CreateSaleSerializer,
     )

import logging
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
User = get_user_model()
debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

factory = APIRequestFactory()
request = factory.get('/')
serializer_context = {
    'request': Request(request),
}


class SaleDetailAPIView(generics.RetrieveAPIView):
    queryset = Sales.objects.all()
    serializer_class = ListSaleSerializer


class SaleCreateAPIView(generics.CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = CreateSaleSerializer

    def perform_create(self, serializer):              
        serializer.save(user=self.request.user)      

        
class SaleListAPIView(generics.ListAPIView):
    serializer_class = ListSaleSerializer

    def get_queryset(self, *args, **kwargs):        
        queryset_list = Sales.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(invoice_number__icontains=query)               
                ).distinct()
        return queryset_list


