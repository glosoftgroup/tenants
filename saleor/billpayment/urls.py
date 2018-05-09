from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

from .api.views import *
from .models import BillPayment as Table

#tax
from saleor.billpayment.tax_api import views as taxViews
from saleor.billpayment.income_api import views as incomeViews


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="billpayment/list.html"), name="index"),
    url(r'^api/create/$', CreateAPIView.as_view(), name='api-create'),
    url(r'^api/delete/(?P<pk>[0-9]+)/$', DestroyView.as_view(), name='api-delete'),
    url(r'^api/list/$', ListAPIView.as_view(), name='api-list'),
    url(r'^api/list/tenant/(?P<pk>[0-9]+)/$', ListAPIView.as_view(), name='tenant-billpayment-api-list'),
    url(r'^api/list/options/$', OptionsListAPIView.as_view(), name='api-list-options'),

    url(r'^api/update/(?P<pk>[0-9]+)/$', UpdateAPIView.as_view(), name='api-update'),
    url(r'^add/$', TemplateView.as_view(template_name="billpayment/form.html"), name='add'),
    url(r'^update/(?P<pk>[0-9]+)/$', UpdateView.as_view(template_name="wing/form.html", model=Table, fields=['id', 'name']),
        name='update'),
    url(r'^invoice/(?P<pk>[0-9]+)/$', UpdateView.as_view(template_name="billpayment/invoice.html", model=Table, fields=['id']),
        name='invoice'),

    # rental income for the room
    url(r'^api/list/room/(?P<rmpk>[0-9]+)/$', ListAPIView.as_view(), name='api-list-room-income'),

    # tax
    url(r'^tax/$', login_required(login_url='/')(TemplateView.as_view(template_name="tax/list.html")), name="tax-index"),
    url(r'^tax/api/list/$', taxViews.ListAPIView.as_view(), name='tax-api-list'),
    url(r'^tax/detail/$', login_required(login_url='/')(TemplateView.as_view(template_name="tax/detail.html")), name="tax-detail"),

    # rental income
    url(r'^income/$', login_required(login_url='/')(TemplateView.as_view(template_name="income/list.html")), name="income-index"),
    url(r'^income/api/list/$', incomeViews.ListAPIView.as_view(), name='income-api-list'),
    url(r'^income/detail/$', login_required(login_url='/')(TemplateView.as_view(template_name="income/detail.html")), name="income-detail"),

]

