from django.forms.models import ModelForm

from hstool.models import Source, Indicator


class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = ['author_id']


class IndicatorForm(ModelForm):
    class Meta:
        model = Indicator
        exclude = ['author_id']

