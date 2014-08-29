from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from hstool.models import Source, Indicator, DriverOfChange


class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = ['author_id']


class IndicatorForm(ModelForm):
    class Meta:
        model = Indicator
        exclude = ['author_id']


class DriverForm(ModelForm):
    class Meta:
        model = DriverOfChange
        exclude = ['author_id']
        labels = {
            "type": _("Type of Driver of Change"),
            "trend_type": _("Type of trend"),
            "steep_category": _("STEEP category"),
            "time_horizon": _("Time horizon"),
            "geographical_scope": _("Georgaphical scale"),
            "short_name": _("Short name*"),
            "name": _("Long name*"),
            "sources": _("Sources*"),
            "figures": _("Figures*"),
            "summary": _("Summary*"),
        }