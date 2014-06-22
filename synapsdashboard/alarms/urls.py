from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from .views import IndexView, AlarmCreateView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create$', AlarmCreateView.as_view(),
        name='create'),
)
