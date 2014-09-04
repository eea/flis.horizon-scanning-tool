from django.shortcuts import redirect
from django.views.generic import (
    TemplateView, ListView, CreateView, DetailView, DeleteView,
)
from django.core.urlresolvers import reverse_lazy, reverse

from hstool.models import (
    Source, Indicator, DriverOfChange, Country, GeographicalScope, Figure,
)
from hstool.forms import (
    SourceForm, IndicatorForm, DriverForm, CountryForm, GeoScopeForm,
    FigureForm,
)


class PostMixin(object):
    def get_success_url(self):
        return self.request.GET.get('next', reverse('home_view'))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect(self.get_success_url())
        else:
            return super(PostMixin, self).post(request, *args, **kwargs)


class Home(TemplateView):
    template_name = 'home.html'


class SourcesListView(ListView):
    template_name = 'tool/sources_list.html'
    model = Source
    context_object_name = 'sources'


class SourcesAddView(PostMixin, CreateView):
    template_name = 'tool/sources_add.html'
    form_class = SourceForm
    success_url = reverse_lazy('sources_list')


class IndicatorsListView(ListView):
    template_name = 'tool/indicators_list.html'
    model = Indicator
    context_object_name = 'indicators'


class IndicatorsAddView(PostMixin, CreateView):
    template_name = 'tool/indicators_add.html'
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators_list')


class DriversListView(ListView):
    template_name = 'tool/drivers_list.html'
    model = DriverOfChange
    context_object_name = 'drivers'


class DriversAddView(PostMixin, CreateView):
    template_name = 'tool/drivers_add.html'
    form_class = DriverForm
    success_url = reverse_lazy('drivers_list')


class FiguresListView(ListView):
    template_name = 'tool/figures_list.html'
    model = Figure
    context_object_name = 'figures'


class FiguresAddView(PostMixin, CreateView):
    template_name = 'tool/figures_add.html'
    form_class = FigureForm
    success_url = reverse_lazy('figures_list')


class CountriesListView(ListView):
    template_name = 'tool/countries_list.html'
    model = Country
    context_object_name = 'countries'


class CountriesAddView(PostMixin, CreateView):
    template_name = 'tool/countries_add.html'
    form_class = CountryForm
    success_url = reverse_lazy('settings:countries_list')


class GeoScopesListView(ListView):
    template_name = 'tool/geo_scopes_list.html'
    model = GeographicalScope
    context_object_name = 'geo_scopes'


class GeoScopesAddView(PostMixin, CreateView):
    template_name = 'tool/geo_scopes_add.html'
    form_class = GeoScopeForm
    success_url = reverse_lazy('settings:geo_scopes_list')


class AddModalMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.pop('model', None)
        self.model = eval(self.model_name)
        return super(AddModalMixin, self).dispatch(request, *args, **kwargs)


class AddModal(AddModalMixin, CreateView):
    template_name = 'tool/add_modal.html'

    def get_form_class(self):
        return eval(self.model_name+'Form')

    def get_success_url(self):
        return reverse(
            'add_modal_success', args=(self.model_name, self.object.id, )
        )


class AddModalSuccess(AddModalMixin, DetailView):
    template_name = 'tool/add_modal_success.html'

    def get_context_data(self, **kwargs):
        context = super(AddModalSuccess, self).get_context_data()
        context.update({'id_field': '#id_'+self.model_name.lower()+'s'})
        return context


class Delete(PostMixin, DeleteView):
    template_name = 'tool/object_delete.html'

    def dispatch(self, request, *args, **kwargs):
        model = kwargs.pop('model', None)
        self.model = eval(model)
        return super(Delete, self).dispatch(request, *args, **kwargs)
