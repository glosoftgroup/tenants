from django.contrib.auth import get_user_model
from .serializers import (
     TerminalListSerializer,    
     )
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from ...sale.models import Terminal

User = get_user_model()


class TerminalListAPIView(generics.ListAPIView):
    serializer_class = TerminalListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Terminal.objects.all()