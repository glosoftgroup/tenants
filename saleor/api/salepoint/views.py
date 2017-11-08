from ...salepoints.models import SalePoint
from .serializers import (
    SalePointListSerializer,
     )
from rest_framework import generics
from django.contrib.auth import get_user_model
User = get_user_model()


class SalePointListAPIView(generics.ListAPIView):
    serializer_class = SalePointListSerializer
    queryset = SalePoint.objects.all()