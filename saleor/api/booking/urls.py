from django.conf.urls import url

from .views import (
                    PaymentListAPIView,
                    BookingListAPIView,
                    RoomBookingListAPIView,
                    CreateAPIView,
                    UpdateAPIView,
                    CheckOutAPIView
                    )


urlpatterns = [
    url(r'^$', BookingListAPIView.as_view(),
        name='api-booking-list'),
    url(r'^create/$', CreateAPIView.as_view(),
        name='api-create'),
    url(r'^update/(?P<pk>[0-9]+)/$', UpdateAPIView.as_view(),
        name='api-update'),
    url(r'^checkout/(?P<pk>[0-9]+)/$', CheckOutAPIView.as_view(),
        name='api-update'),
    url(r'^customer/(?P<pk>[0-9]+)/$', BookingListAPIView.as_view(),
        name='api-customer-booking-list'),
    url(r'^room/(?P<pk>[0-9]+)/$', RoomBookingListAPIView.as_view(),
        name='api-room-booking-list'),
    url(r'^payments/(?P<pk>[0-9]+)/$', PaymentListAPIView.as_view(),
        name='api-booking-payment-list'),
]

