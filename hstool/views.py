import json

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView,
    TemplateView)
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, Http404
from django.db.models import Q

from braces.views import JSONResponseMixin, AjaxResponseMixin

from hstool.definitions import CANONICAL_ROLES

from hstool.models import (
    Source, DriverOfChange, Figure, Indicator,
    Assessment, Relation, Implication, Impact, GenericElement
)
from flis_metadata.common.models import GeographicalScope

from hstool.forms import (
    SourceForm, DriverForm,
    FigureForm, AssessmentForm, RelationForm,
    ImplicationForm, ImpactForm, IndicatorForm,
    IndicatorFilesFormset
)
from hstool.utils import get_nodes_from_components


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('hstool.config'):
            raise PermissionDenied()
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class OwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        is_admin = request.user.has_perm('hstool.config')
        obj = self.get_object()
        if not is_admin and obj.author_id != request.user.username:
            raise PermissionDenied()
        return super(OwnerRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class ListMixin(ListView):
    def get_queryset(self, queryset=None):
        is_admin = self.request.user.has_perm('hstool.config')
        queryset = self.model._default_manager.all()

        if not is_admin:
            queryset = queryset.filter(
                Q(draft=False) | Q(author_id=self.request.user.username)
            )

        return queryset


class AuthorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.author_id = request.user.username
        return super(AuthorMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author_id = self.author_id
        return super(AuthorMixin, self).form_valid(form)


class HomeView(TemplateView):
    template_name = 'tool/home.html'


class AssessmentsList(ListMixin):
    template_name = 'tool/assessments_list.html'
    model = Assessment
    context_object_name = 'assessments'


class AssessmentsDetail(OwnerRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = 'tool/assessments_detail.html'
    model = Assessment
    context_object_name = 'assessment'


def assessments_relations(request, pk):
    relations = get_object_or_404(Assessment, pk=pk).relations.all()
    nodes = []
    for relation in relations:
        nodes.append(relation.source)
        nodes.append(relation.destination)
    nodes = sorted(set(nodes), key=lambda el: el.id)

    data = {'nodes': [], 'links': []}
    for node in nodes:
        (model, subtitle, subtitle_color) = (
            ('impacts', 'Impact', 0) if hasattr(node, 'impact') else
            ('drivers', node.driverofchange.get_trend_type_display(),
             node.driverofchange.trend_type)
        )
        url = reverse(
            'modals:relations_detail',
            kwargs={'model': model, 'pk': node.id, 'assessment_pk': pk}
        )
        data['nodes'].append({
            'url': url,
            'title': node.name,
            'subtitle': subtitle,
            'subtitle_color': subtitle_color,
            #'figures': [figure.name for figure in node.figures.all()],
        })
    ids_map = {}
    for (d3_id, db_id) in enumerate([node.id for node in nodes]):
        ids_map[db_id] = d3_id

    for relation in relations:
        url = reverse(
            'modals:relations_detail',
            kwargs={'model': 'relations', 'pk': relation.id,
                    'assessment_pk': pk}
        )
        data['links'].append({
            'url': url,
            'source': ids_map[relation.source.id],
            'target': ids_map[relation.destination.id],
            'type': relation.relationship_type,
        })

    comp_nodes = get_nodes_from_components(nodes, relations)

    if len(comp_nodes) > 1:
        for i in range(len(comp_nodes)):
            data['links'].append({
                'source': ids_map[comp_nodes[i - 1]],
                'target': ids_map[comp_nodes[i]],
                'type': 3,
            })

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


class AssessmentsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/assessments_add.html'
    form_class = AssessmentForm

    def get_success_url(self):
        return reverse('assessments:detail', kwargs={'pk': self.object.pk})


class AssessmentsUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/assessments_add.html'
    model = Assessment
    form_class = AssessmentForm
    context_object_name = 'assessment'

    def get_success_url(self):
        return reverse('assessments:detail', kwargs={'pk': self.object.pk})


class AssessmentsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Assessment
    success_url = reverse_lazy('home_view')


class RelationsMixin(object):
    DESTINATION_TYPE_OPTIONS = {
        "driver": "Driver of change",
        "impact": "Impact",
    }

    def dispatch(self, request, *args, **kwargs):
        assessment_pk = kwargs.pop('assessment_pk', None)
        self.assessment = get_object_or_404(Assessment, pk=assessment_pk)
        is_admin = request.user.has_perm('hstool.config')
        if not is_admin and self.assessment.author_id != request.user.username:
            raise PermissionDenied()
        return super(RelationsMixin, self).dispatch(request, *args, **kwargs)


class RelationsAdd(RelationsMixin, CreateView):
    template_name = 'tool/relation_add.html'
    form_class = RelationForm
    model = Relation

    def get_context_data(self, **kwargs):
        context = super(RelationsAdd, self).get_context_data(**kwargs)
        context['assessment'] = self.assessment
        context['destination_types'] = self.DESTINATION_TYPE_OPTIONS
        context['show_driver_of_change_check'] = "false"
        context['show_impact_check'] = "false"
        return context

    def get_form_kwargs(self):
        data = super(RelationsAdd, self).get_form_kwargs()
        data['assessment'] = self.assessment
        return data

    def get_success_url(self):
        return reverse('assessments:detail', kwargs={'pk': self.assessment.id})


class RelationsUpdate(RelationsMixin, UpdateView):
    template_name = 'tool/relation_add.html'
    model = Relation
    form_class = RelationForm

    def get_success_url(self):
        return reverse('assessments:detail',
                       kwargs={'pk': self.object.assessment.pk})

    def get_context_data(self, **kwargs):
        context = super(RelationsUpdate, self).get_context_data(**kwargs)
        context['assessment'] = self.object.assessment
        context['destination_types'] = self.DESTINATION_TYPE_OPTIONS
        context['show_driver_of_change_check'] = "false"
        context['show_impact_check'] = "false"
        if self.object.destination.is_driver():
            context['show_driver_of_change_check'] = "true"
        if self.object.destination.is_impact():
            context['show_impact_check'] = "true"
        return context


class RelationsDelete(RelationsMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Relation

    def get_success_url(self):
        return reverse('assessments:detail',
                       kwargs={'pk': self.object.assessment.id})


class RelationsList(LoginRequiredMixin, ListView):
    template_name = 'tool/relation_list.html'
    model = Relation
    context_object_name = 'relations'

    def dispatch(self, request, *args, **kwargs):
        assessment_pk = kwargs.pop('assessment_pk', None)
        self.assessment = get_object_or_404(Assessment, pk=assessment_pk)
        return super(RelationsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, queryset=None):
        is_admin = self.request.user.has_perm('hstool.config')
        queryset = self.model._default_manager.all()
        if not is_admin:
            queryset = queryset.filter(
                Q(draft=False) | Q(author_id=self.request.user.username) &
                Q(assessment=self.assessment)
            )

        return queryset


class SourcesList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/sources_list.html'
    model = Source
    context_object_name = 'sources'


class SourcesAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/sources_add.html'
    form_class = SourceForm
    success_url = reverse_lazy('sources:list')


class SourcesUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/sources_add.html'
    model = Source
    form_class = SourceForm
    success_url = reverse_lazy('sources:list')


class SourcesDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Source
    success_url = reverse_lazy('sources:list')


class DriversList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/drivers_list.html'
    model = DriverOfChange
    context_object_name = 'drivers'


class DriversAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/drivers_add.html'
    form_class = DriverForm
    success_url = reverse_lazy('drivers:list')


class DriversUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/drivers_add.html'
    model = DriverOfChange
    form_class = DriverForm
    success_url = reverse_lazy('drivers:list')

    def get_context_data(self, **kwargs):
        context = super(DriversUpdate, self).get_context_data(**kwargs)
        geographical_scope = self.object.geographical_scope
        context['required'] = (
            geographical_scope.require_country if geographical_scope else None)
        return context


class DriversDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = DriverOfChange
    success_url = reverse_lazy('drivers:list')


class ImplicationsList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/implications_list.html'
    model = Implication
    context_object_name = 'implications'


class ImplicationsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/implications_add.html'
    form_class = ImplicationForm
    success_url = reverse_lazy('implications:list')


class ImplicationsUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/implications_add.html'
    model = Implication
    form_class = ImplicationForm
    success_url = reverse_lazy('implications:list')

    def get_context_data(self, **kwargs):
        context = super(ImplicationsUpdate, self).get_context_data(**kwargs)
        geographical_scope = self.object.geographical_scope
        context['required'] = (
            geographical_scope.require_country if geographical_scope else None)
        return context


class ImplicationsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Implication
    success_url = reverse_lazy('implications:list')


class FiguresList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/figures_list.html'
    model = Figure
    context_object_name = 'figures'


class FiguresAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/figures_add.html'
    form_class = FigureForm
    success_url = reverse_lazy('figures:list')


class FiguresUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/figures_add.html'
    model = Figure
    form_class = FigureForm
    success_url = reverse_lazy('figures:list')


class FiguresDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Figure
    success_url = reverse_lazy('figures:list')


class ImpactsList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/impacts_list.html'
    model = Impact
    context_object_name = 'impacts'


class ImpactsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/impacts_add.html'
    form_class = ImpactForm
    success_url = reverse_lazy('impacts:list')


class ImpactsUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/impacts_add.html'
    model = Impact
    form_class = ImpactForm
    success_url = reverse_lazy('impacts:list')


class ImpactsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Impact
    success_url = reverse_lazy('impacts:list')


class IndicatorsList(LoginRequiredMixin, ListMixin):
    template_name = 'tool/indicators_list.html'
    model = Indicator
    context_object_name = 'indicators'


class IndicatorsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/indicators_add.html'
    model = Indicator
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators:list')

    def get_context_data(self, **kwargs):
        context = super(IndicatorsAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            context['files_form'] = IndicatorFilesFormset(self.request.POST,
                                                          self.request.FILES)
            context['empty_form'] = context['files_form'].empty_form
        else:
            context['files_form'] = IndicatorFilesFormset()
            context['empty_form'] = context['files_form'].empty_form
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        files_form = context['files_form']
        if form.is_valid() and files_form.is_valid():
            self.object = form.save()
            files_form.instance = self.object
            files_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class IndicatorsUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/indicators_add.html'
    model = Indicator
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators:list')

    def get_context_data(self, **kwargs):
        context = super(IndicatorsUpdate, self).get_context_data(**kwargs)
        geographical_scope = self.object.geographical_scope
        context['required'] = (
            geographical_scope.require_country if geographical_scope else None)

        if self.request.POST:
            context['files_form'] = IndicatorFilesFormset(self.request.POST,
                                                          self.request.FILES,
                                                          instance=self.object)
            context['empty_form'] = context['files_form'].empty_form

        else:
            context['files_form'] = IndicatorFilesFormset(instance=self.object)
            context['empty_form'] = context['files_form'].empty_form
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        files_form = context['files_form']
        if form.is_valid() and files_form.is_valid():
            self.object = form.save()
            files_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class IndicatorsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = Indicator
    success_url = reverse_lazy('indicators:list')


class GeoScopesRequired(JSONResponseMixin, AjaxResponseMixin, DetailView):

    model = GeographicalScope

    def get_object(self):
        pk = self.request.GET.get('geo_scope_id')
        if pk:
            return get_object_or_404(GeographicalScope, pk=int(pk))
        return Http404

    def get_ajax(self, request, *args, **kwargs):
        return self.render_json_response({
            'required': self.get_object().require_country,
        })


class RolesOverview(AdminRequiredMixin, TemplateView):
    template_name = 'settings/roles.html'

    def get_context_data(self, **kwargs):
        context = {}
        roles = []

        def has_perm(group, perm):
            return perm in ['%s.%s' % (p.content_type.app_label, p.codename)
                            for p in group.permissions.all()]

        for role in CANONICAL_ROLES:
            group, new = Group.objects.get_or_create(name=role)
            roles.append(dict(name=role,
                              config=has_perm(group, 'hstool.config'),
                              create=has_perm(group, 'hstool.create'),
                              view=True))
        context['roles'] = roles
        return context


class ModelMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.pop('model', None)
        self.model = self.url_to_models.get(self.model_name)
        return super(ModelMixin, self).dispatch(request, *args, **kwargs)


class AddModal(ModelMixin, AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'modals/add_generic_model.html'

    url_to_models = {
        'sources': Source,
        'figures': Figure,
        'indicators': Indicator,
    }

    urls_to_forms = {
        'sources': SourceForm,
        'figures': FigureForm,
        'indicators': IndicatorForm,
    }

    def get_form_class(self):
        self.model_name = self.kwargs.get('model')
        return self.urls_to_forms.get(self.model_name)

    def get_success_url(self):
        return reverse(
            'modals:add_success', args=(self.model_name, self.object.id, )
        )


class AddModalSuccess(ModelMixin, AuthorMixin, LoginRequiredMixin, DetailView):
    template_name = 'modals/add_generic_model_success.html'

    url_to_models = {
        'sources': Source,
        'figures': Figure,
        'indicators': Indicator,
    }

    def get_context_data(self, **kwargs):
        context = super(AddModalSuccess, self).get_context_data()
        context.update({'model_name': self.model_name})
        return context


class ViewModal(DetailView):
    url_to_models = {
        'figures': Figure,
        'drivers': DriverOfChange,
        'relations': Relation,
        'indicators': Indicator,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.pop('model', None)
        self.model = self.url_to_models.get(self.model_name)
        if self.model is Figure:
            self.template_name = 'modals/view_figure.html'
        elif self.model is DriverOfChange:
            self.template_name = 'modals/view_driver.html'
        else:
            self.template_name = 'modals/view_relation.html'
        self.assessment_pk = kwargs.pop('assessment_pk', None)
        return super(ViewModal, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewModal, self).get_context_data(**kwargs)
        context.update({
            'type': self.model_name,
            'current_assessment': get_object_or_404(Assessment,
                                                    pk=self.assessment_pk)
        })
        return context


class ViewFigureModal(LoginRequiredMixin, DetailView):
    template_name = 'modals/view_figure.html'
    model = Figure
    context_object_name = 'figure'


class UserEntriesView(LoginRequiredMixin, ListView):
    template_name = 'user_entries.html'
    model = GenericElement
    context_object_name = 'elements'


class UserEntriesDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'object_delete.html'
    model = GenericElement
    success_url = reverse_lazy('entries:list')
