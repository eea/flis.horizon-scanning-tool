from django.shortcuts import redirect
from django.views.generic import (
    TemplateView, ListView, CreateView, DetailView, DeleteView,
)
from django.core.urlresolvers import reverse_lazy, reverse

from hstool.models import (
    Source, Indicator, DriverOfChange, Country, GeographicalScope
)
from hstool.forms import (
    SourceForm, IndicatorForm, DriverForm, CountryForm, GeoScopeForm,
)


class Home(TemplateView):
    template_name = 'home.html'


class SourcesListView(ListView):
    template_name = 'tool/sources_list.html'
    model = Source
    context_object_name = 'sources'


class SourcesAddView(CreateView):
    template_name = 'tool/sources_add.html'
    form_class = SourceForm
    success_url = reverse_lazy('sources_list')


class IndicatorsListView(ListView):
    template_name = 'tool/indicators_list.html'
    model = Indicator
    context_object_name = 'indicators'


class IndicatorsAddView(CreateView):
    template_name = 'tool/indicators_add.html'
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators_list')

    def get_context_data(self, **kwargs):
        context = super(IndicatorsAddView, self).get_context_data(**kwargs)
        context.update({'source_form': SourceForm})
        return context


class DriversListView(ListView):
    template_name = 'tool/drivers_list.html'
    model = DriverOfChange
    context_object_name = 'drivers'


class DriversAddView(CreateView):
    template_name = 'tool/drivers_add.html'
    form_class = DriverForm
    success_url = reverse_lazy('drivers_list')


class CountriesListView(ListView):
    template_name = 'tool/countries_list.html'
    model = Country
    context_object_name = 'countries'


class CountriesAddView(CreateView):
    template_name = 'tool/countries_add.html'
    form_class = CountryForm
    success_url = reverse_lazy('settings:countries_list')


class GeoScopesListView(ListView):
    template_name = 'tool/geo_scopes_list.html'
    model = GeographicalScope
    context_object_name = 'geo_scopes'


class GeoScopesAddView(CreateView):
    template_name = 'tool/geo_scopes_add.html'
    form_class = GeoScopeForm
    success_url = reverse_lazy('settings:geo_scopes_list')


class SourceAddModal(CreateView):
    template_name = 'tool/sources_add_modal.html'
    model = Source
    form_class = SourceForm

    def get_success_url(self):
        source = self.object
        return reverse('sources_add_modal_success', args=(source.id, ))


class SourceAddModalSuccess(DetailView):
    template_name = 'tool/sources_add_modal_success.html'
    model = Source


class Delete(DeleteView):
    models_dict = {
        'Source': Source,
        'DriverOfChange': DriverOfChange,
        'Indicator': Indicator,
    }

    template_name = 'tool/object_delete.html'

    def dispatch(self, request, *args, **kwargs):
        model = kwargs.pop('model', None)
        self.model = self.models_dict.get(model)
        return super(Delete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home_view'))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect(self.get_success_url())
        else:
            return super(Delete, self).post(request, *args, **kwargs)
