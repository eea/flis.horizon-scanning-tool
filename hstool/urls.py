from django.conf.urls import patterns, include, url

from django.contrib import admin
from hstool.views import Home, SourcesListView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home_view'),
    url(r'^sources/list/$', SourcesListView.as_view(), name='sources_list'),

    url(r'^admin/', include(admin.site.urls)),
)
