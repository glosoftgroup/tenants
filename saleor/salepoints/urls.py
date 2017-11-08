from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from . import views, paginate, pdf
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', permission_required('salepoints.view_salepoint', login_url='not_found')
    (views.points), name='salepoints'),
    url(r'^add/$', permission_required('salepoints.add_salepoint', login_url='not_found')
    (views.add_point), name='salepoints-add'),
    url(r'^edit/(?P<pk>[0-9]+)/$', permission_required('salepoints.change_salepoint', login_url='not_found')(views.edit_point), name='salepoint-edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('salepoints.delete_salepoint')
                (views.delete_point), name='salepoints-delete'),
    url(r'^paginagte/$',paginate.paginate_point, name='salepoints-paginate'),
    url(r'^search/$',paginate.search_point, name='salepoints-search'),
    url( r'^points/pdf/$', pdf.pdf, name ='salepoints_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)