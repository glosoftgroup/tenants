from django.conf.urls import url

from .views import (
    OrderCreateAPIView,
    OrderListAPIView,
    OrderStatusListAPIView,
    SalePointOrdersListAPIView,
    TableOrdersListAPIView,
    )


urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(),
     name='list-orders'),
    url(r'^create-order/$',
        OrderCreateAPIView.as_view(), name='create-order'),
    url(r'^search/status/$', OrderStatusListAPIView.as_view(),
     name='search-orders'),
    url(r'^sale-point/(?P<pk>[0-9]+)$', SalePointOrdersListAPIView.as_view(), name='api-sale_point-orders'),
    url(r'^table/(?P<pk>[0-9]+)$', TableOrdersListAPIView.as_view(), name='api-table-orders'),

]

