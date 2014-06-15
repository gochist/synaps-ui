from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from .views import IndexView, MonitoringView, GraphView 


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<tenant_id>[^/]+)/monitoring$',
        MonitoringView.as_view(), name='monitoring'),
    url(r'^graph/$',
        GraphView.as_view(), name='graph'),
)
