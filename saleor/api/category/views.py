from ...product.models import Category
from rest_framework.request import Request
from .serializers import (
    CategoryListSerializer,
     )
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class SalePointCategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()

    def list(self, request, pk=None):
        serializer_context = {
            'request': Request(request),
        }
        queryset = self.get_queryset().filter(sale_point__pk=pk)
        serializer = CategoryListSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

