from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from .api.views import *
from .models import Bill as Table


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="bill/list.html"), name="index"),
    url(r'^api/create/$', CreateAPIView.as_view(), name='api-create'),
    url(r'^api/delete/(?P<pk>[0-9]+)/$', DestroyView.as_view(), name='api-delete'),
    url(r'^api/list/$', ListAPIView.as_view(), name='api-list'),
    url(r'^api/list/(?P<pk>[0-9]+)/$', ListAPIView.as_view(), name='tenant-bill-api-list'),
    url(r'^api/list/tenants/$', TenantsListAPIView.as_view(), name='api-list-tenants'),

    url(r'^api/update/(?P<pk>[0-9]+)/$', UpdateAPIView.as_view(), name='api-update'),
    url(r'^add/$', TemplateView.as_view(template_name="bill/form.html"), name='add'),
    url(r'^update/(?P<pk>[0-9]+)/$', UpdateView.as_view(template_name="bill/form.html", model=Table, fields=['id']),
        name='update'),
    url(r'^invoice/(?P<pk>[0-9]+)/$', UpdateView.as_view(template_name="bill/invoice.html", model=Table, fields=['id']),
        name='invoice'),
]

