from django.conf.urls import url

from .views import (
    OrderCreateAPIView,
    OrderListAPIView
    )


urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(),
     name='list-orders'),
    url(r'^create-order/$',
        OrderCreateAPIView.as_view(), name='create-order'),
    

]

