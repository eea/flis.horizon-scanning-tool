from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from hstool.models import (
    Source, Indicator, DriverOfChange, Country, GeographicalScope, Figure,
)


class SourceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs["cols"] = 70
        self.fields['summary'].widget.attrs["rows"] = 6

    class Meta:
        model = Source
        exclude = ['author_id']
        labels = {
            "title": _("Title in English"),
            "title_original": _("Title in original language"),
            "published_year": _("Year of publication"),
            "url": _("URL"),
        }


class IndicatorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['figures'].widget.attrs["size"] = 6

    class Meta:
        model = Indicator
        exclude = ['author_id']
        labels = {
            "theme": _("Thematic category"),
            "timeline": _("Time coverage"),
            "year_base": _("Base year*"),
            "year_end": _("End year"),
            "geographical_scope": _("Georgaphical scale"),
            "short_name": _("Short name"),
            "name": _("Long name"),
            "sources": _("Sources"),
            "figures": _("Figures"),
            "url": _("URL"),
        }


class DriverForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs["cols"] = 70
        self.fields['summary'].widget.attrs["rows"] = 6
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['figures'].widget.attrs["size"] = 6

    class Meta:
        model = DriverOfChange
        exclude = ['author_id']
        labels = {
            "type": _("Type of Driver of Change"),
            "trend_type": _("Type of trend"),
            "steep_category": _("STEEP category"),
            "time_horizon": _("Time horizon"),
            "geographical_scope": _("Georgaphical scale"),
            "short_name": _("Short name"),
            "name": _("Long name"),
            "sources": _("Sources"),
            "figures": _("Figures"),
            "summary": _("Summary"),
            "url": _("URL"),
        }


class FigureForm(ModelForm):
    class Meta:
        model = Figure
        exclude = ['author_id']


class CountryForm(ModelForm):
    class Meta:
        model = Country
        labels = {
            "iso": _("ISO"),
        }


class CountryUpdateForm(ModelForm):
    class Meta:
        model = Country
        exclude = ['iso']


class GeoScopeForm(ModelForm):
    class Meta:
        model = GeographicalScope
