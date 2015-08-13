from django.forms.models import ModelForm, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import ModelChoiceField
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime

from hstool.models import (
    Source, DriverOfChange, Figure, Indicator,
    Assessment, Relation, Implication, GenericElement,
    Impact, IndicatorFiles
)
from flis_metadata.common.models import (
    Country, EnvironmentalTheme, GeographicalScope
)


class GeoScopeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeoScopeForm, self).__init__(*args, **kwargs)
        self.fields['country'].queryset = (
            Country.objects.filter(is_deleted=False)
        )

        self.fields['geographical_scope'].queryset = (
            GeographicalScope.objects.filter(is_deleted=False)
        )

    def clean(self):
        cleaned_data = super(GeoScopeForm, self).clean()
        geo_scope = cleaned_data['geographical_scope']
        country = cleaned_data['country']
        if geo_scope and geo_scope.require_country and not country:
            self._errors["country"] = self.error_class([
                'The selected Geographical Scale requires a country.'
            ])
            del cleaned_data["country"]
        return cleaned_data


class AssessmentForm(GeoScopeForm):
    def __init__(self, *args, **kwargs):
        super(AssessmentForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs["cols"] = 70
        self.fields['description'].widget.attrs["rows"] = 6
        self.fields['title'].widget.attrs["size"] = 30

    class Meta:
        model = Assessment
        exclude = ['author_id']


class SourceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs["cols"] = 70
        self.fields['summary'].widget.attrs["rows"] = 6
        self.fields['name'].widget.attrs["size"] = 30
        self.fields['title_original'].widget.attrs["size"] = 60
        self.fields['author'].widget.attrs["size"] = 30
        self.fields['url'].widget.attrs["size"] = 60

    class Meta:
        model = Source
        exclude = ['author_id', 'short_name']
        labels = {
            "name": _("Title in English"),
            "title_original": _("Title in original language"),
            "published_year": _("Year of publication"),
            "url": _("URL"),
        }

    def clean(self):
        cleaned_data = super(SourceForm, self).clean()
        try:
            self._errors['published_year']
        except KeyError:
            try:
                year = int(cleaned_data['published_year'])
                if year not in range(1000, 9999):
                    self._errors['published_year'] = "This field must be an year."
                    del cleaned_data['published_year']
            except ValueError:
                self._errors['published_year'] = "This field must be an year."
                del cleaned_data['published_year']
        return cleaned_data


class RelationForm(ModelForm):
    driver = ModelChoiceField(queryset=DriverOfChange.objects.all(),
                              required=False)
    impact = ModelChoiceField(queryset=Impact.objects.all(),
                              required=False)

    class Meta:
        model = Relation
        exclude = ['assessment']
        labels = {
            "source": _("Select a driver of change, the starting point of the relation"),
            "destination": _("Select the end item"),
            "relationship_type": _("Select type of relation"),
            "description": _("Relation description"),
            "figures": _("Append facts and/or figures to illustrate relation"),
            "indicators": _("Indicators"),
        }

    def __init__(self, *args, **kwargs):
        self.assessment = kwargs.pop('assessment', None)
        super(RelationForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs["rows"] = 6
        try:
            if self.instance.destination.is_driver():
                self.fields['driver'].initial = DriverOfChange.objects.get(
                    pk=self.instance.destination.driverofchange.pk)
            if self.instance.destination.is_impact():
                self.fields['impact'].initial = Impact.objects.get(
                    pk=self.instance.destination.impact.pk)
        except GenericElement.DoesNotExist:
            return

    def clean(self):
        cleaned_data = super(RelationForm, self).clean()
        if self.cleaned_data['driver']:
            self.cleaned_data['destination'] = self.cleaned_data['driver']
        elif self.cleaned_data['impact']:
            self.cleaned_data['destination'] = self.cleaned_data['impact']
        else:
            self._errors["destination"] = self.error_class([
                'This field is required.'
            ])
            del cleaned_data["destination"]
        return cleaned_data

    def save(self):
        relation = super(RelationForm, self).save(commit=False)
        if self.assessment:
            relation.assessment = self.assessment
        relation.save()
        self.save_m2m()
        return relation


class DriverForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs["cols"] = 70
        self.fields['summary'].widget.attrs["rows"] = 6
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['figures'].widget.attrs["size"] = 6
        self.fields['indicators'].widget.attrs["size"] = 6
        self.fields['impacts'].widget.attrs["size"] = 6
        self.fields['short_name'].widget.attrs["size"] = 30
        self.fields['name'].widget.attrs["size"] = 60
        self.fields['url'].widget.attrs["size"] = 100

        self.fields['country'].queryset = (
            Country.objects.filter(is_deleted=False)
        )
        self.fields['geographical_scope'].queryset = (
            GeographicalScope.objects.filter(is_deleted=False)
        )

    class Meta:
        model = DriverOfChange
        exclude = ['author_id', 'implications']
        labels = {
            "type": _("Type of Driver of Change"),
            "trend_type": _("Type of trend"),
            "uncertainty_type": _("Type of uncertainty"),
            "steep_category": _("STEEP category"),
            "geographical_scope": _("Geographical scale"),
            "name": _("Long name"),
            "url": _("URL"),
            "figures": _("Facts and figures"),
            "impacts": _("Impacts"),
            "indicators": _("Indicators"),
        }

    def clean(self):
        cleaned_data = super(DriverForm, self).clean()
        geo_scope = cleaned_data['geographical_scope']
        country = cleaned_data['country']
        if geo_scope and geo_scope.require_country and not country:
            self._errors["country"] = self.error_class([
                'The selected Geographical Scale requires a country.'
            ])
            del cleaned_data["country"]

        return cleaned_data


def _file_help_text():
    def _get_extension(file_name, separator='/'):
        return '.' + file_name.split(separator)[1]

    text = 'Supported file types: '
    file_types = settings.SUPPORTED_FILES_FACTS_AND_FIGURES

    return text + (', '.join(map(_get_extension, file_types)) or
                   'any type')


class FigureForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FigureForm, self).__init__(*args, **kwargs)
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['url'].widget.attrs["size"] = 100
        self.fields['theme'].queryset = (EnvironmentalTheme.objects.filter(is_deleted=False))

    class Meta:
        model = Figure
        exclude = ['author_id', 'short_name', 'geographical_scope', 'country']
        fields = ['name', 'theme', 'sources', 'file', 'url']
        labels = {
            "theme": _("Thematic category"),
            "url": _("URL"),
            "sources": _("Source"),
            "name": _("Title"),
        }
        help_texts = {
            'file': _(_file_help_text()),
            'sources': _("Choose from list of sources. "),
        }


class ImplicationForm(GeoScopeForm):
    class Meta:
        model = Implication
        exclude = ['author_id', 'short_name', 'url', 'figures']
        labels = {
            "policy_area": _("Area of policy"),
            "geographical_scope": _("Geographical scale"),
            "name": _("Title"),
        }

    def __init__(self, *args, **kwargs):
        super(ImplicationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs["size"] = 30
        self.fields['description'].widget.attrs["cols"] = 70
        self.fields['description'].widget.attrs["rows"] = 6


class ImpactForm(GeoScopeForm):
    class Meta:
        model = Impact
        exclude = ['author_id', 'url', 'figures']
        labels = {
            'impact_type': _("Type of impact"),
            'geographical_scope': _("Geographical scale"),
            'steep_category': _("STEEP category"),
            'name': _("Long name"),
            'short_name': _("Short name"),
            'sources': _("Source"),
        }
        help_texts = {
            'name': _("Understandable name for non-experts"),
            'short_name': _("Acronym for expert use"),
            'sources': _("Choose from list of sources. "),
        }

    def __init__(self, *args, **kwargs):
        super(ImpactForm, self).__init__(*args, **kwargs)

        self.fields['short_name'].widget.attrs["size"] = 30
        self.fields['name'].widget.attrs["size"] = 60
        self.fields['sources'].required = True


class IndicatorForm(GeoScopeForm):
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['name'].widget.attrs["size"] = 60
        self.fields['theme'].queryset = (
            EnvironmentalTheme.objects.filter(is_deleted=False)
        )

    class Meta:
        model = Indicator
        exclude = ['short_name', 'url', 'author_id']
        fields = ['name', 'theme', 'geographical_scope', 'country',
                  'start_date', 'end_date', 'sources', 'assessment',
                  'assessment_author']
        labels = {
            "theme": _("Thematic category"),
            "start_date": _("Start date"),
            "end_date": _("End date"),
            "geographical_scope": _("Georgaphical scale"),
            "name": _("Title"),
            "assessment": _("Assessment"),
            "assessment_author": _("Assessment author"),
        }

IndicatorFilesFormset = inlineformset_factory(Indicator, IndicatorFiles, extra=1,
                                              max_num=5)
