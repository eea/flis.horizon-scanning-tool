from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView,
)
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from hstool.models import (
    Source, Indicator, DriverOfChange, Country, GeographicalScope, Figure,
    Assessment, Relation
)
from hstool.forms import (
    SourceForm, IndicatorForm, DriverForm, CountryForm, GeoScopeForm,
    FigureForm, CountryUpdateForm, AssessmentForm, RelationForm
)


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('hstool.config'):
            raise PermissionDenied()
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        is_admin = request.user.has_perm('hstool.config')
        obj = self.get_object()
        if not is_admin and obj.author_id != request.user.username:
            raise PermissionDenied()
        return super(OwnerRequiredMixin, self).dispatch(request, *args, **kwargs)


class AuthorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.author_id = request.user.username
        return super(AuthorMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author_id = self.author_id
        return super(AuthorMixin, self).form_valid(form)


class AssessmentsList(ListView):
    template_name = 'tool/assessments_list.html'
    model = Assessment
    context_object_name = 'assessments'


class AssessmentsDetail(DetailView):
    template_name = 'tool/assessments_detail.html'
    model = Assessment
    context_object_name = 'assessment'

    def get_context_data(self, **kwargs):
        context = super(AssessmentsDetail, self).get_context_data(**kwargs)
        context['relations'] = Relation.objects.filter(assessment=self.object)
        return context


class AssessmentsPreview(AssessmentsDetail):

    template_name = 'tool/assessments_preview.html'


class AssessmentsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/assessments_add.html'
    form_class = AssessmentForm

    def get_success_url(self):
        return reverse_lazy('assessments:detail',
                            kwargs={'pk': self.object.pk})


class AssessmentsUpdate( OwnerRequiredMixin, UpdateView):
    template_name = 'tool/assessments_add.html'
    model = Assessment
    form_class = AssessmentForm
    success_url = reverse_lazy('home_view')


class AssessmentsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'tool/object_delete.html'
    model = Assessment
    success_url = reverse_lazy('assessments:list')


class RelationAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/relation_add.html'
    form_class = RelationForm
    model = Relation

    def dispatch(self, request, assessment_pk):
        self.assessment = get_object_or_404(Assessment, pk=assessment_pk)
        return super(RelationAdd, self).dispatch(request, assessment_pk)

    def get_context_data(self, **kwargs):
        context = super(RelationAdd, self).get_context_data(**kwargs)
        context['assessment'] = self.assessment
        return context

    def get_form_kwargs(self):
        data = super(RelationAdd, self).get_form_kwargs()
        data['assessment'] = self.assessment
        return data

    def get_success_url(self):
        return reverse_lazy('assessments:detail',
                            kwargs={'pk': self.assessment.id})


class RelationList(LoginRequiredMixin, ListView):
    template_name = 'tool/relation_list.html'
    model = Relation
    context_object_name = 'relations'

    def dispatch(self, request, assessment_pk):
        self.assessment = get_object_or_404(Assessment, pk=assessment_pk)
        return super(RelationList, self).dispatch(request, assessment_pk)

    def get_queryset(self):
        return Relation.objects.filter(assessment=self.assessment)


class SourcesList(LoginRequiredMixin, ListView):
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
    template_name = 'tool/object_delete.html'
    model = Source
    success_url = reverse_lazy('sources:list')


class IndicatorsList(LoginRequiredMixin, ListView):
    template_name = 'tool/indicators_list.html'
    model = Indicator
    context_object_name = 'indicators'


class IndicatorsAdd(AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/indicators_add.html'
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators:list')


class IndicatorsUpdate(OwnerRequiredMixin, UpdateView):
    template_name = 'tool/indicators_add.html'
    model = Indicator
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators:list')


class IndicatorsDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'tool/object_delete.html'
    model = Indicator
    success_url = reverse_lazy('indicators:list')


class DriversList(LoginRequiredMixin, ListView):
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


class DriversDelete(OwnerRequiredMixin, DeleteView):
    template_name = 'tool/object_delete.html'
    model = DriverOfChange
    success_url = reverse_lazy('drivers:list')


class FiguresList(LoginRequiredMixin, ListView):
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
    template_name = 'tool/object_delete.html'
    model = Figure
    success_url = reverse_lazy('figures:list')


class CountriesList(AdminRequiredMixin, ListView):
    template_name = 'tool/countries_list.html'
    model = Country
    context_object_name = 'countries'


class CountriesAdd(AdminRequiredMixin, CreateView):
    template_name = 'tool/countries_add.html'
    form_class = CountryForm
    success_url = reverse_lazy('settings:countries_list')


class CountriesUpdate(AdminRequiredMixin, UpdateView):

    template_name = 'tool/countries_update.html'
    model = Country
    form_class = CountryUpdateForm
    success_url = reverse_lazy('settings:countries_list')


class CountriesDelete(AdminRequiredMixin, DeleteView):
    template_name = 'tool/object_delete.html'
    model = Country
    success_url = reverse_lazy('settings:countries_list')


class GeoScopesList(AdminRequiredMixin, ListView):
    template_name = 'tool/geo_scopes_list.html'
    model = GeographicalScope
    context_object_name = 'geo_scopes'


class GeoScopesAdd(AdminRequiredMixin, CreateView):
    template_name = 'tool/geo_scopes_add.html'
    form_class = GeoScopeForm
    success_url = reverse_lazy('settings:geo_scopes_list')


class GeoScopesUpdate(AdminRequiredMixin, UpdateView):
    template_name = 'tool/geo_scopes_add.html'
    model = GeographicalScope
    form_class = GeoScopeForm
    success_url = reverse_lazy('settings:geo_scopes_list')


class GeoScopesDelete(AdminRequiredMixin, DeleteView):
    template_name = 'tool/object_delete.html'
    model = GeographicalScope
    success_url = reverse_lazy('settings:geo_scopes_list')


class ModelMixin(object):
    url_to_models = {
        'sources': Source,
        'figures': Figure,
        'indicators': Indicator,
        'drivers': DriverOfChange,
        'countries': Country,
        'geo_scales': GeographicalScope,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.pop('model', None)
        self.model = self.url_to_models.get(self.model_name)
        return super(ModelMixin, self).dispatch(request, *args, **kwargs)


class AddModal(ModelMixin, AuthorMixin, LoginRequiredMixin, CreateView):
    template_name = 'tool/add_modal.html'

    urls_to_forms = {
        'sources': SourceForm,
        'figures': FigureForm,
    }

    def get_form_class(self):
        self.model_name = self.kwargs.get('model')
        return self.urls_to_forms.get(self.model_name)

    def get_success_url(self):
        return reverse(
            'add_modal_success', args=(self.model_name, self.object.id, )
        )


class AddModalSuccess(ModelMixin, AuthorMixin, LoginRequiredMixin, DetailView):
    template_name = 'tool/add_modal_success.html'

    def get_context_data(self, **kwargs):
        context = super(AddModalSuccess, self).get_context_data()
        context.update({'model_name': self.model_name})
        return context
