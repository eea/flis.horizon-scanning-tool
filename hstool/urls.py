from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from hstool.views import (
    SourcesList, SourcesAdd, IndicatorsList, IndicatorsAdd, DriversList,
    DriversAdd, CountriesList, CountriesAdd, GeoScopesList, GeoScopesAdd,
    AddModal, AddModalSuccess, FiguresList, FiguresAdd, SourcesUpdate,
    IndicatorsUpdate, DriversUpdate, FiguresUpdate, CountriesUpdate,
    GeoScopesUpdate, SourcesDelete, IndicatorsDelete, FiguresDelete,
    DriversDelete, CountriesDelete, GeoScopesDelete, AssessmentsList,
    AssessmentsAdd, AssessmentsUpdate, AssessmentsDelete, AssessmentsDetail,
    RelationAdd, AssessmentsPreview, RelationUpdate, RelationDelete,
    RolesOverview, GeoScopesRequired, EnvironmentalThemeList,
    EnvironmentalThemeAdd, EnvironmentalThemeUpdate, EnvironmentalThemeDelete,
    assessments_relations, ViewModal,
)


admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^countries/list/$', CountriesList.as_view(),
        name='countries_list'),
    url(r'^countries/add/$', CountriesAdd.as_view(), name='countries_add'),
    url(r'^countries/update/(?P<pk>\w+)$', CountriesUpdate.as_view(),
        name='countries_update'),
    url(r'^countries/delete/(?P<pk>\w+)$', CountriesDelete.as_view(),
        name='countries_delete'),

    url(r'^geographic_scopes/list/$', GeoScopesList.as_view(),
        name='geo_scopes_list'),
    url(r'^geographic_scopes/add/$', GeoScopesAdd.as_view(),
        name='geo_scopes_add'),
    url(r'^geographic_scopes/update/(?P<pk>\d+)/$', GeoScopesUpdate.as_view(),
        name='geo_scopes_update'),
    url(r'^geographic_scopes/delete/(?P<pk>\d+)/$', GeoScopesDelete.as_view(),
        name='geo_scopes_delete'),
    url(r'^geographic_scopes/required/$',
        GeoScopesRequired.as_view(), name='geo_scopes_required'),

    url(r'^themes/list/$', EnvironmentalThemeList.as_view(),
        name='themes_list'),
    url(r'^themes/add/$', EnvironmentalThemeAdd.as_view(),
        name='themes_add'),
    url(r'^themes/update/(?P<pk>\d+)/$', EnvironmentalThemeUpdate.as_view(),
        name='themes_update'),
    url(r'^themes/delete/(?P<pk>\d+)/$', EnvironmentalThemeDelete.as_view(),
        name='themes_delete'),

    url(r'^roles/$', RolesOverview.as_view(), name='roles'),
)

sources_urls = patterns(
    '',
    url(r'^list/$', SourcesList.as_view(), name='list'),
    url(r'^add/$', SourcesAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', SourcesUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', SourcesDelete.as_view(), name='delete'),
)

indicators_urls = patterns(
    '',
    url(r'^list/$', IndicatorsList.as_view(), name='list'),
    url(r'^add/$', IndicatorsAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', IndicatorsUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', IndicatorsDelete.as_view(), name='delete'),
)

drivers_urls = patterns(
    '',
    url(r'^list/$', DriversList.as_view(), name='list'),
    url(r'^add/$', DriversAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', DriversUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', DriversDelete.as_view(), name='delete'),
)

figures_urls = patterns(
    '',
    url(r'^list/$', FiguresList.as_view(), name='list'),
    url(r'^add/$', FiguresAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', FiguresUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', FiguresDelete.as_view(), name='delete'),
)

assessments_urls = patterns(
    '',
    url(r'^add/$', AssessmentsAdd.as_view(), name='add'),
    url(r'^detail/(?P<pk>\d+)/$', AssessmentsDetail.as_view(), name='detail'),
    url(r'^detail/(?P<pk>\d+)/relations$', assessments_relations,
        name='relations'),
    url(r'^preview/(?P<pk>\d+)/$', AssessmentsPreview.as_view(),
        name='preview'),
    url(r'^update/(?P<pk>\d+)/$', AssessmentsUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', AssessmentsDelete.as_view(), name='delete'),
)

relations_urls = patterns(
    '',
    url(r'(?P<assessment_pk>\d+)/add/$', RelationAdd.as_view(), name='add'),
    url(r'(?P<pk>\d+)/update/$', RelationUpdate.as_view(),
        name='update'),
    url(r'(?P<pk>\d+)/delete/$', RelationDelete.as_view(), name='delete')
)

modals_urls = patterns(
    '',
    url(r'^detail/(?P<assessment_pk>\d+)/(?P<model>\w+)/(?P<pk>\d+)/$',
        ViewModal.as_view(), name='relations_detail'),
)

urlpatterns = patterns(
    '',
    url(r'^$', AssessmentsList.as_view(), name='home_view'),

    url(r'^assessment/', include(assessments_urls, namespace='assessments')),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^assessment/relation/',
        include(relations_urls, namespace='relations')),

    url(r'^sources/', include(sources_urls, namespace='sources')),

    url(r'^indicators/', include(indicators_urls, namespace='indicators')),

    url(r'^docs/', include(drivers_urls, namespace='drivers')),

    url(r'^figures/', include(figures_urls, namespace='figures')),

    url(r'^modals/', include(modals_urls, namespace='modals')),

    url(r'^(?P<model>\w+)/add/modal/$', AddModal.as_view(), name='add_modal'),
    url(r'^(?P<model>\w+)/add/modal/success/(?P<pk>\d+)$',
        AddModalSuccess.as_view(), name='add_modal_success'),

    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
