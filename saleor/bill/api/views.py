from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import pagination
from .pagination import PostLimitOffsetPagination

from saleor.bill.models import Bill as Table
from saleor.booking.models import Book
from .serializers import (
    CreateListSerializer,
    TableListSerializer,
    UpdateSerializer,
    TenantsListSerializer
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
                queryset_list = Table.objects.all.select_related()
        except Exception as e:
            queryset_list = Table.objects.all()

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(page_size)
        else:
            pagination.PageNumberPagination.page_size = 10
        if self.request.GET.get('month'):
            queryset_list = queryset_list.filter(month__icontains=self.request.GET.get('month'))
        if self.request.GET.get('status') and self.request.GET.get('status') != 'all':
            queryset_list = queryset_list.filter(status=self.request.GET.get('status'))

        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(customer__name__icontains=query) |
                Q(room__name__icontains=query) |
                Q(billtype__name__icontains=query))
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


class TenantsListAPIView(generics.ListAPIView):
    """
        tenants list details
        GET /api/list/tenants/
    """
    serializer_class = TenantsListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PostLimitOffsetPagination

    def get_serializer_context(self):
        if self.request.GET.get('date'):
            return {"date": self.request.GET.get('date'), 'request': self.request}
        return {"date": None, 'request': self.request}

    def get_queryset(self, *args, **kwargs):
        queryset_list = Book.objects.filter(active=True, room__is_booked=True)

        return queryset_list.order_by('-id')
