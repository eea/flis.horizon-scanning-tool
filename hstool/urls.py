from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from hstool.views import (
    Home, SourcesListView, SourcesAddView, IndicatorsListView,
    IndicatorsAddView, DriversListView, DriversAddView, CountriesListView,
    CountriesAddView, GeoScopesListView, GeoScopesAddView, AddModal,
    AddModalSuccess, FiguresListView, FiguresAddView, SourcesUpdate,
    IndicatorsUpdate, DriversUpdate, FiguresUpdate, CountriesUpdate,
    GeoScopesUpdate, SourcesDelete, IndicatorsDelete, FiguresDelete, DriversDelete, CountriesDelete, GeoScopesDelete,
)

admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^countries/list/$', CountriesListView.as_view(),
        name='countries_list'),
    url(r'^countries/add/$', CountriesAddView.as_view(), name='countries_add'),
    url(r'^countries/update/(?P<pk>\w+)$', CountriesUpdate.as_view(),
        name='countries_update'),
    url(r'^countries/delete/(?P<pk>\w+)$', CountriesDelete.as_view(),
        name='countries_delete'),

    url(r'^geographic_scopes/list/$', GeoScopesListView.as_view(),
        name='geo_scopes_list'),
    url(r'^geographic_scopes/add/$', GeoScopesAddView.as_view(),
        name='geo_scopes_add'),
    url(r'^geographic_scopes/update/(?P<pk>\d+)/$', GeoScopesUpdate.as_view(),
        name='geo_scopes_update'),
    url(r'^geographic_scopes/delete/(?P<pk>\d+)/$', GeoScopesDelete.as_view(),
        name='geo_scopes_delete'),

)

sources_urls = patterns(
    '',
    url(r'^list/$', SourcesListView.as_view(), name='list'),
    url(r'^add/$', SourcesAddView.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', SourcesUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', SourcesDelete.as_view(), name='delete'),
)

indicators_urls = patterns(
    '',
    url(r'^list/$', IndicatorsListView.as_view(), name='list'),
    url(r'^add/$', IndicatorsAddView.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', IndicatorsUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', IndicatorsDelete.as_view(), name='delete'),
)

drivers_urls = patterns(
    '',
    url(r'^list/$', DriversListView.as_view(), name='list'),
    url(r'^add/$', DriversAddView.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', DriversUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', DriversDelete.as_view(), name='delete'),
)

figures_urls = patterns(
    '',
    url(r'^list/$', FiguresListView.as_view(), name='list'),
    url(r'^add/$', FiguresAddView.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', FiguresUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', FiguresDelete.as_view(), name='delete'),
)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home_view'),

    url(r'^settings/', include(settings_urls, namespace='settings')),


    url(r'^sources/', include(sources_urls, namespace='sources')),

    url(r'^indicators/', include(indicators_urls, namespace='indicators')),

    url(r'^docs/', include(drivers_urls, namespace='drivers')),

    url(r'^figures/', include(figures_urls, namespace='figures')),

    url(r'^(?P<model>\w+)/add/modal/$', AddModal.as_view(), name='add_modal'),
    url(r'^(?P<model>\w+)/add/modal/success/(?P<pk>\d+)$',
        AddModalSuccess.as_view(), name='add_modal_success'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
