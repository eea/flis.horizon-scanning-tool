from django.conf.urls import patterns, include, url

from django.contrib import admin
from hstool.views import (
    Home, SourcesListView, SourcesAddView, IndicatorsListView,
    IndicatorsAddView,
)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home_view'),
    url(r'^sources/list/$', SourcesListView.as_view(), name='sources_list'),
    url(r'^sources/add/$', SourcesAddView.as_view(), name='sources_add'),
    url(r'^indicator/list/$', IndicatorsListView.as_view(),
        name='indicators_list'),
    url(r'^indicator/add/$', IndicatorsAddView.as_view(),
        name='indicators_add'),

    url(r'^admin/', include(admin.site.urls)),
)
