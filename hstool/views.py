from django.views.generic import TemplateView, ListView, CreateView
from django.core.urlresolvers import reverse_lazy

from hstool.models import Source
from hstool.forms import SourceForm


class Home(TemplateView):
    template_name = 'home.html'


class SourcesListView(ListView):
    template_name = 'tool/sources_list.html'
    model = Source
    context_object_name = 'sources'

    def get_queryset(self):
        return Source.objects.all()


class SourcesAddView(CreateView):
    template_name = 'tool/sources_add.html'
    form_class = SourceForm
    success_url = reverse_lazy('sources_list')

