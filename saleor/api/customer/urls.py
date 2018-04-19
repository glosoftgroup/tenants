from django.conf.urls import url

from .views import (
    CustomerListAPIView,
    CustomerDetailAPIView,
    CreditWorthyCustomerListAPIView,
    CustomerUpdateAPIView,
    CustomerPagListAPIView,
    PaymentListAPIView
    )


urlpatterns = [
   url(r'^$', CustomerListAPIView.as_view(), name='customer-list'),
   url(r'^backend/$', CustomerPagListAPIView.as_view(), name='list'),
   url(r'^details/(?P<pk>[0-9]+)/$', CustomerDetailAPIView.as_view(), name='customer-detail'),
   url(r'^credit-worthy/$', CreditWorthyCustomerListAPIView.as_view(), name='credit-worthy-customers'),
   url(r'^redeem-points/(?P<pk>[0-9]+)/$', CustomerUpdateAPIView.as_view(),name='update-customer-details-api'), 
   #payments   
   url(r'^payments/$', PaymentListAPIView.as_view(), name='api-payment-list'),
   url(r'^payments/(?P<pk>[0-9]+)/$', PaymentListAPIView.as_view(), name='api-customer-payment-list')
]

