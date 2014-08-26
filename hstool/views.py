from django.views.generic import TemplateView, ListView
from hstool.models import Source


class Home(TemplateView):
    template_name = 'home.html'


class SourcesListView(ListView):
    template_name = 'tool/sources_list.html'
    model = Source
