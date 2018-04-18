from django.conf.urls import url

from .views import (
                    MaintenanceListAPIView,
                    RoomMaintenanceListAPIView,
                    )


urlpatterns = [
    url(r'^$', MaintenanceListAPIView.as_view(),
        name='api-maintenance-list'),
    url(r'^room/(?P<pk>[0-9]+)/$', RoomMaintenanceListAPIView.as_view(),
        name='api-room-maintenance-list'),
]

