from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from hstool.models import (
    Source, Indicator, DriverOfChange, Figure,
    Assessment, Relation, Implication,
)
from flis_metadata.common.models import (
    Country, EnvironmentalTheme, GeographicalScope
)


class AssessmentForm(ModelForm):
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
        self.fields['title'].widget.attrs["size"] = 30
        self.fields['title_original'].widget.attrs["size"] = 60
        self.fields['author'].widget.attrs["size"] = 30
        self.fields['url'].widget.attrs["size"] = 60

    class Meta:
        model = Source
        exclude = ['author_id']
        labels = {
            "title": _("Title in English"),
            "title_original": _("Title in original language"),
            "published_year": _("Year of publication"),
            "url": _("URL"),
        }


class RelationForm(ModelForm):

    class Meta:
        model = Relation
        exclude = ['assessment']

    def __init__(self, *args, **kwargs):
        self.assessment = kwargs.pop('assessment', None)
        super(RelationForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs["rows"] = 6

    def save(self):
        relation = super(RelationForm, self).save(commit=False)
        if self.assessment:
            relation.assessment = self.assessment
        relation.save()
        self.save_m2m()
        return relation


class IndicatorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['figures'].widget.attrs["size"] = 6
        self.fields['url'].widget.attrs["size"] = 100
        self.fields['short_name'].widget.attrs["size"] = 30
        self.fields['name'].widget.attrs["size"] = 60

        self.fields['country'].queryset = (
            Country.objects.filter(is_deleted=False)
        )
        self.fields['theme'].queryset = (
            EnvironmentalTheme.objects.filter(is_deleted=False)
        )
        self.fields['geographical_scope'].queryset = (
            GeographicalScope.objects.filter(is_deleted=False)
        )

    class Meta:
        model = Indicator
        exclude = ['author_id']
        labels = {
            "theme": _("Thematic category"),
            "year_base": _("Base year"),
            "year_end": _("End year"),
            "geographical_scope": _("Georgaphical scale"),
            "name": _("Long name"),
            "url": _("URL"),
        }

    def clean(self):
        cleaned_data = super(IndicatorForm, self).clean()
        geo_scope = cleaned_data['geographical_scope']
        country = cleaned_data['country']
        if geo_scope and geo_scope.require_country and not country:
            self._errors["country"] = self.error_class([
                'The selected Geographical Scale requires a country.'
            ])
            del cleaned_data["country"]

        return cleaned_data


class DriverForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs["cols"] = 70
        self.fields['summary'].widget.attrs["rows"] = 6
        self.fields['sources'].widget.attrs["size"] = 6
        self.fields['figures'].widget.attrs["size"] = 6
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
        exclude = ['author_id']
        labels = {
            "type": _("Type of Driver of Change"),
            "trend_type": _("Type of trend"),
            "uncertainty_type": _("Type of uncertainty"),
            "steep_category": _("STEEP category"),
            "geographical_scope": _("Geographical scale"),
            "name": _("Long name"),
            "url": _("URL"),
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

    class Meta:
        model = Figure
        exclude = ['author_id']

        help_texts = {
            'file': _(_file_help_text()),
        }


class ImplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImplicationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs["size"] = 30
        self.fields['description'].widget.attrs["cols"] = 70
        self.fields['description'].widget.attrs["rows"] = 6

        self.fields['country'].queryset = (
            Country.objects.filter(is_deleted=False)
        )
        self.fields['geographical_scope'].queryset = (
            GeographicalScope.objects.filter(is_deleted=False)
        )

    class Meta:
        model = Implication
        exclude = ['author_id', 'short_name', 'name', 'url', 'figures']
        labels = {
            "policy_area": _("Area of policy"),
            "geographical_scope": _("Geographical scale"),
        }

    def clean(self):
        cleaned_data = super(ImplicationForm, self).clean()
        geo_scope = cleaned_data['geographical_scope']
        country = cleaned_data['country']
        if geo_scope and geo_scope.require_country and not country:
            self._errors["country"] = self.error_class([
                'The selected Geographical Scale requires a country.'
            ])
            del cleaned_data["country"]

        return cleaned_data
