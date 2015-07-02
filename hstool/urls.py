from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from hstool import views


admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^geographic_scopes/required/$',
        views.GeoScopesRequired.as_view(), name='geo_scopes_required'),
    url(r'^roles/$', views.RolesOverview.as_view(), name='roles'),
)

sources_urls = patterns(
    '',
    url(r'^list/$', views.SourcesList.as_view(), name='list'),
    url(r'^add/$', views.SourcesAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.SourcesUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.SourcesDelete.as_view(), name='delete'),
)

indicators_urls = patterns(
    '',
    url(r'^list/$', views.IndicatorsList.as_view(), name='list'),
    url(r'^add/$', views.IndicatorsAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.IndicatorsUpdate.as_view(),
        name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.IndicatorsDelete.as_view(),
        name='delete'),
)

drivers_urls = patterns(
    '',
    url(r'^list/$', views.DriversList.as_view(), name='list'),
    url(r'^add/$', views.DriversAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.DriversUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.DriversDelete.as_view(), name='delete'),
)

implications_urls = patterns(
    '',
    url(r'^list/$', views.ImplicationsList.as_view(), name='list'),
    url(r'^add/$', views.ImplicationsAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.ImplicationsUpdate.as_view(),
        name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.ImplicationsDelete.as_view(),
        name='delete'),
)

figures_urls = patterns(
    '',
    url(r'^list/$', views.FiguresList.as_view(), name='list'),
    url(r'^add/$', views.FiguresAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.FiguresUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.FiguresDelete.as_view(), name='delete'),
)

impacts_urls = patterns(
    '',
    url(r'^list/$', views.ImpactsList.as_view(), name='list'),
    url(r'^add/$', views.ImpactsAdd.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.ImpactsUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.ImpactsDelete.as_view(), name='delete'),
)

assessments_urls = patterns(
    '',
    url(r'^add/$', views.AssessmentsAdd.as_view(), name='add'),
    url(r'^detail/(?P<pk>\d+)/$', views.AssessmentsDetail.as_view(),
        name='detail'),
    url(r'^detail/(?P<pk>\d+)/relations$', views.assessments_relations,
        name='relations'),
    url(r'^preview/(?P<pk>\d+)/$', views.AssessmentsPreview.as_view(),
        name='preview'),
    url(r'^update/(?P<pk>\d+)/$', views.AssessmentsUpdate.as_view(),
        name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.AssessmentsDelete.as_view(),
        name='delete'),
)

relations_urls = patterns(
    '',
    url(r'add/$', views.RelationsAdd.as_view(), name='add'),
    url(r'update/(?P<pk>\d+)/$', views.RelationsUpdate.as_view(),
        name='update'),
    url(r'delete/(?P<pk>\d+)/$', views.RelationsDelete.as_view(), name='delete')
)

modals_urls = patterns(
    '',
    url(r'^detail/(?P<assessment_pk>\d+)/(?P<model>\w+)/(?P<pk>\d+)/$',
        views.ViewModal.as_view(), name='relations_detail'),
    url(r'^add/(?P<model>\w+)/$', views.AddModal.as_view(), name='add'),
    url(r'^add/success/(?P<model>\w+)/(?P<pk>\d+)$',
        views.AddModalSuccess.as_view(),
        name='add_success'),
    url(r'^view/figure/(?P<pk>\d+)/$', views.ViewFigureModal.as_view(),
        name='view_figure'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.AssessmentsList.as_view(), name='home_view'),

    url(r'^assessments/', include(assessments_urls, namespace='assessments')),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^assessments/(?P<assessment_pk>\d+)/relations/',
        include(relations_urls, namespace='relations')),

    url(r'^sources/', include(sources_urls, namespace='sources')),

    url(r'^indicators/', include(indicators_urls, namespace='indicators')),

    url(r'^docs/', include(drivers_urls, namespace='drivers')),

    url(r'^implications/', include(implications_urls, namespace='implications')),

    url(r'^figures/', include(figures_urls, namespace='figures')),

    url(r'^impacts/', include(impacts_urls, namespace='impacts')),

    url(r'^modals/', include(modals_urls, namespace='modals')),

    url(r'^_lastseencount/$', 'frame.utils.get_objects_from_last_seen_count'),

    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
