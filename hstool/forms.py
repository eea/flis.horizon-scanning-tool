from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from hstool.models import Source, Indicator, DriverOfChange, Country


class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = ['author_id']
        labels = {
            "title": _("Title in English"),
            "title_original": _("Title in original language"),
            "published_year": _("Year of publication"),
            "path": _("Upload file"),
            "url": _("URL"),
        }


class IndicatorForm(ModelForm):
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
            "sources": _("Source"),
            "figures": _("Figures"),
            "url": _("URL"),
        }


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
            "short_name": _("Short name"),
            "name": _("Long name"),
            "sources": _("Sources"),
            "figures": _("Figures"),
            "summary": _("Summary"),
            "url": _("URL"),
        }


class CountryForm(ModelForm):
    class Meta:
        model = Country
        labels = {
            "iso": _("ISO"),
        }