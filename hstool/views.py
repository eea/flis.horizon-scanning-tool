from django.views.generic import TemplateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy

from hstool.models import (
    Source, Indicator, DriverOfChange,
)
from hstool.forms import SourceForm, IndicatorForm


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
    template_name = 'tool/indicator_add.html'
    form_class = IndicatorForm
    success_url = reverse_lazy('indicators_list')


class DriversListView(ListView):
    template_name = 'tool/drivers_list.html'
    model = DriverOfChange
    context_object_name = 'drivers'
