from ...product.models import Category
from .serializers import (
    CategoryListSerializer,
     )
from rest_framework import generics
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()