from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # paymentoption urls
    url(r'^$', permission_required('sale.view_table', login_url='account_login')
            (views.list), name='table-list'),
    url(r'^add/$', permission_required('sale.add_paymentoption', login_url='account_login')
            (views.add), name='table-add'),
    url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('sale.delete_paymentoption', login_url='account_login')
            (views.delete), name='table-delete'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='table-detail'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.edit, name='update-table'),
    url( r'^search/$', views.searchs, name = 'table-search' ),
    url(r'^paginate/', views.paginate, name='table_paginate'),
    
    ]

if settings.DEBUG:
    # urlpatterns += [ url(r'^static/(?P<path>.*)$', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)