from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from hstool.views import (
    Home, SourcesListView, SourcesAddView, IndicatorsListView,
    IndicatorsAddView, DriversListView, DriversAddView, CountriesListView,
    CountriesAddView, GeoScopesListView, GeoScopesAddView, AddModal,
    AddModalSuccess, Delete, FiguresListView, FiguresAddView, SourcesUpdate,
    IndicatorsUpdate, DriversUpdate, FiguresUpdate, CountriesUpdate,
    GeoScopesUpdate,
)

admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^countries/list/$', CountriesListView.as_view(),
        name='countries_list'),
    url(r'^countries/add/$', CountriesAddView.as_view(), name='countries_add'),
    url(r'^countries/update/(?P<iso>\w+)$', CountriesUpdate.as_view(),
        name='countries_update'),

    url(r'^geographic_scopes/list/$', GeoScopesListView.as_view(),
        name='geo_scopes_list'),
    url(r'^geographic_scopes/add/$', GeoScopesAddView.as_view(),
        name='geo_scopes_add'),
    url(r'^geographic_scopes/update/(?P<pk>\d+)/$', GeoScopesUpdate.as_view(),
        name='geo_scopes_update'),

)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home_view'),
    url(r'^sources/list/$', SourcesListView.as_view(), name='sources_list'),
    url(r'^sources/add/$', SourcesAddView.as_view(), name='sources_add'),
    url(r'^sources/update/(?P<pk>\d+)/$', SourcesUpdate.as_view(),
        name='sources_update'),

    url(r'^indicators/list/$', IndicatorsListView.as_view(),
        name='indicators_list'),
    url(r'^indicators/add/$', IndicatorsAddView.as_view(),
        name='indicators_add'),
    url(r'^indicators/update/(?P<pk>\d+)/$', IndicatorsUpdate.as_view(),
        name='indicators_update'),

    url(r'^docs/list/$', DriversListView.as_view(), name='drivers_list'),
    url(r'^docs/add/$', DriversAddView.as_view(), name='drivers_add'),
    url(r'^docs/update/(?P<pk>\d+)/$', DriversUpdate.as_view(),
        name='drivers_update'),

    url(r'^figures/list/$', FiguresListView.as_view(), name='figures_list'),
    url(r'^figures/add/$', FiguresAddView.as_view(), name='figures_add'),
    url(r'^figures/update/(?P<pk>\d+)/$', FiguresUpdate.as_view(),
        name='figures_update'),

    url(r'^(?P<model>\w+)/add/modal/$', AddModal.as_view(), name='add_modal'),
    url(r'^(?P<model>\w+)/add/modal/success/(?P<pk>\d+)$',
        AddModalSuccess.as_view(), name='add_modal_success'),

    url(r'^delete/(?P<model>\w+)/(?P<pk>\w+)/$', Delete.as_view(),
        name='delete_record'),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
