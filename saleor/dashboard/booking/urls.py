from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # paymentoption urls
    url(r'^$', permission_required('room.view_room', login_url='account_login')
        (views.listing), name='booking-list'),
    url(r'^add/$', permission_required('room.add_room', login_url='account_login')
        (views.add), name='booking-add'),
    url(r'^book/$', views.book, name='booking-rooms'),
    url(r'^charts/$', views.charts, name='booking-charts'),
    url(r'^occupied/$', views.occupied_rooms, name='room-occupied'),
    url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('room.delete_room', login_url='account_login')
        (views.delete), name='booking-delete'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='booking-detail'),
    url(r'^invoice/(?P<pk>[0-9]+)/$', views.invoice, name='booking-invoice'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.edit, name='booking-edit'),
    url(r'^pay/', views.pay, name='invoice-pay'),
    url(r'compute/price/$', views.compute_room_price, name="compute-room-price"),
    url(r'fetch/amenities/$', views.fetch_amenities, name="fetch-rooms"),
    url(r'fetch/customers/$', views.customer_token, name="fetch-customers-token"),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)