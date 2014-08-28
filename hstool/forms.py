from django.forms.models import ModelForm

from hstool.models import Source


class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = ['author_id']
