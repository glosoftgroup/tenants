from rest_framework.response import Response
from rest_framework.request import Request
from ...table.models import Table
from .serializers import (
    TableListSerializer,
     )
from rest_framework import generics
from django.contrib.auth import get_user_model
User = get_user_model()


class TableListAPIView(generics.ListAPIView):
    serializer_class = TableListSerializer
    queryset = Table.objects.all()


class SalePointTableListAPIView(generics.ListAPIView):
    serializer_class = TableListSerializer
    queryset = Table.objects.all()

    def list(self, request, pk=None):
        serializer_context = {
            'request': Request(request),
        }
        queryset = self.get_queryset().filter(sale_point__pk=pk)
        serializer = TableListSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

