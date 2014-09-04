from django.conf.urls import patterns, include, url

from django.contrib import admin
from hstool.views import (
    Home, SourcesListView, SourcesAddView, IndicatorsListView,
    IndicatorsAddView, DriversListView, DriversAddView, CountriesListView,
    CountriesAddView, GeoScopesListView, GeoScopesAddView,
    AddModal, AddModalSuccess, Delete, FiguresListView, FiguresAddView,
)

admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^countries/list/$', CountriesListView.as_view(),
        name='countries_list'),

    url(r'^countries/add/$', CountriesAddView.as_view(), name='countries_add'),

    url(r'^geographic_scopes/list/$', GeoScopesListView.as_view(),
        name='geo_scopes_list'),

    url(r'^geographic_scopes/add/$', GeoScopesAddView.as_view(),
        name='geo_scopes_add'),

)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home_view'),
    url(r'^sources/list/$', SourcesListView.as_view(), name='sources_list'),
    url(r'^sources/add/$', SourcesAddView.as_view(), name='sources_add'),

    url(r'^indicators/list/$', IndicatorsListView.as_view(),
        name='indicators_list'),
    url(r'^indicators/add/$', IndicatorsAddView.as_view(),
        name='indicators_add'),

    url(r'^docs/list/$', DriversListView.as_view(), name='drivers_list'),
    url(r'^docs/add/$', DriversAddView.as_view(), name='drivers_add'),

    url(r'^facts/list/$', FiguresListView.as_view(), name='figures_list'),
    url(r'^facts/add/$', FiguresAddView.as_view(), name='figures_add'),

    url(r'^(?P<model>Source|Figure)/add/modal/$', AddModal.as_view(),
        name='add_modal'),
    url(r'^(?P<model>Source|Figure)/add/modal/success/(?P<pk>\d+)$',
        AddModalSuccess.as_view(), name='add_modal_success'),

    url(r'^delete/(?P<model>'
        'Source|'
        'Indicator|'
        'DriverOfChange|'
        'Figure|'
        'Country|'
        'GeographicalScope|'
        ')/(?P<pk>\d+)/$', Delete.as_view(), name='delete_record'),

    url(r'^delete/(?P<model>Country)/(?P<pk>[a-z][a-z])/$', Delete.as_view(),
        name='delete_record'),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^admin/', include(admin.site.urls)),
)
