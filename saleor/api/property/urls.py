from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', ListAPIView.as_view(), name='api-list'),
    url(r'^wing/$', ListWingAPIView.as_view(), name='api-list-wing'),
    url(r'^image/$', ListImagesAPIView.as_view(), name='api-list-images')
]

