from django.conf.urls import url

from .views import (
    SalePointListAPIView
    )


urlpatterns = [
    url(r'^$', SalePointListAPIView.as_view(), name='api-sale_point-list'),
]

