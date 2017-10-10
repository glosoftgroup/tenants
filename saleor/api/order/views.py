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
    ListOrderSerializer,
    OrderSerializer,
    OrderUpdateSerializer
     )
from ...decorators import user_trail
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
# context=serializer_context


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
    queryset = Orders.objects.all()
    serializer_class = ListOrderSerializer(instance=queryset, context=serializer_context)

    def list(self, request, pk=None):
        serializer_context = {
            'request': Request(request),
        }
        # Note the use of `get_queryset()` instead of `self.queryset`
        query = self.request.GET.get('q')
        if query:
            queryset = self.get_queryset().filter(table__pk=pk).filter(status=query)
        else:
            queryset = self.get_queryset().filter(table__pk=pk)
        serializer = ListOrderSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)


class OrderUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderUpdateSerializer

    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user)
        if instance.status == 'fully-paid':
            send_to_sale(instance)
        user_trail(self.request.user.name,
                   'made a sale:#' + str(serializer.data['invoice_number']) + ' sale worth: ' + str(
                       serializer.data['total_net']), 'add')
        info_logger.info(
            'User: ' + str(self.request.user) + ' made a credit sale:' + str(serializer.data['invoice_number']))
        terminal = Terminal.objects.get(pk=int(serializer.data['terminal']))
        trail = 'User: ' + str(self.request.user) + \
                ' updated a credited sale :' + str(serializer.data['invoice_number']) + \
                ' Net#: ' + str(serializer.data['total_net']) + \
                ' Amount paid#:' + str(serializer.data['amount_paid'])

        TerminalHistoryEntry.objects.create(
            terminal=terminal,
            comment=trail,
            crud='deposit',
            user=self.request.user
        )
        DrawerCash.objects.create(
                                 manager=self.request.user,
                                 user=self.request.user,
                                 terminal=terminal,
                                 amount=serializer.data['amount_paid'],
                                 trans_type='credit paid')


def send_to_sale(credit):
    sale = Sales.objects.create(
        user=credit.user,
        invoice_number=credit.invoice_number,
        total_net=credit.total_net,
        sub_total=credit.sub_total,
        balance=credit.balance,
        terminal=credit.terminal,
        amount_paid=credit.amount_paid,
        status=credit.status,
        total_tax=credit.total_tax,
    )
    for item in credit.items():
        new_item = SoldItem.objects.create(
                                       sales=sale,
                                       sku=item.sku,
                                       quantity=item.quantity,
                                       product_name=item.product_name,
                                       total_cost=item.total_cost,
                                       unit_cost=item.unit_cost,
                                       product_category=item.product_category
                                       )
        print new_item
