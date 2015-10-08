from django.views.generic import ListView, DetailView
from hstool.models import DriverOfChange


class DocList(ListView):
    template_name = 'public/doc_list.html'
    model = DriverOfChange

    def get_queryset(self):
        return self.model.objects.filter(draft=False)
