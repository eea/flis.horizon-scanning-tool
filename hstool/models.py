from datetime import datetime
from django.db.models import (
    Model, CharField, IntegerField, TextField, ForeignKey, BooleanField,
    ManyToManyField, FileField, DateField,
    DateTimeField)
from django.forms.forms import ValidationError
from django.conf import settings

from hstool.definitions import (
    DOC_TYPE_CHOICES, DOC_TREND_TYPE_CHOICES,
    DOC_TIME_HORIZON_CHOICES,
    RELATION_TYPE_CHOICES, DOC_UNCERTAINTIES_TYPE_CHOICES,
    IMPACT_TYPES,
)
from hstool.utils import (
    path_and_rename_sources, path_and_rename_figures,
    path_and_rename_indicators
)


class ContentTypeRestrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args,
                                                                 **kwargs)

        def _get_extension(file_name, separator='/'):
            return '.' + file_name.split(separator)[1]

        if not self.content_types or not hasattr(data.file, 'content_type'):
            return data

        content_type = data.file.content_type

        if content_type not in self.content_types:
            if content_type == 'application/unknown':
                extensions = map(_get_extension, self.content_types)
                if _get_extension(data.file.name, '.') in extensions:
                    return data

            raise ValidationError(
                'File type not supported: {0}'.format(content_type))

        return data

    def south_field_triple(self):
        return (
            'hstool.models.ContentTypeRestrictedFileField',
            [],
            dict(content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES)
        )


class SourcesMixin(Model):
    sources = ManyToManyField('Source', blank=True, null=True)

    class Meta:
        abstract = True


class FiguresMixin(Model):
    figures = ManyToManyField('Figure', blank=True, null=True)

    class Meta:
        abstract = True


class SteepCategory(Model):
    title = CharField(max_length=64)
    short_title = CharField(max_length=5)
    author_id = CharField(max_length=64)

    def __unicode__(self):
        return self.title


class GenericElement(Model):
    draft = BooleanField(default=True)
    author_id = CharField(max_length=64)
    short_name = CharField(max_length=64)
    name = CharField(max_length=512)
    geographical_scope = ForeignKey('common.GeographicalScope',
                                    null=True, blank=True)
    country = ForeignKey('common.Country', null=True, blank=True)
    url = CharField(max_length=256, blank=True, null=True)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

    def is_driver(self):
        try:
            if self.driverofchange:
                return True
        except DriverOfChange.DoesNotExist:
            return False
        return False

    def is_impact(self):
        try:
            if self.impact:
                return True
        except Impact.DoesNotExist:
            return False
        return False

    def __unicode__(self):
        return self.name


class Source(GenericElement):
    title_original = CharField(max_length=512)
    published_year = IntegerField()
    author = CharField(max_length=512)
    file = FileField(upload_to=path_and_rename_sources)
    summary = TextField(max_length=2048)

    def __unicode__(self):
        return self.name


class Figure(GenericElement, SourcesMixin):
    file = ContentTypeRestrictedFileField(
        upload_to=path_and_rename_figures,
        content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES,
    )
    theme = ForeignKey('common.EnvironmentalTheme')


class Indicator(GenericElement, SourcesMixin):
    theme = ForeignKey('common.EnvironmentalTheme')
    start_date = DateField(editable=True, null=True, blank=True)
    end_date = DateField(editable=True)
    assessment = TextField(null=True, blank=True)
    assessment_author = CharField(max_length=64, null=True, blank=True)


class IndicatorFiles (Model):
    file = FileField(
        upload_to=path_and_rename_indicators,
        null=True, blank=True
    )
    indicator = ForeignKey(Indicator)


class DriverOfChange(GenericElement, FiguresMixin, SourcesMixin):
    type = IntegerField(choices=DOC_TYPE_CHOICES)
    trend_type = IntegerField(choices=DOC_TREND_TYPE_CHOICES,
                              default=1)
    uncertainty_type = IntegerField(choices=DOC_UNCERTAINTIES_TYPE_CHOICES,
                                    default=1)
    steep_category = ForeignKey('SteepCategory', related_name='driver_category')
    time_horizon = IntegerField(choices=DOC_TIME_HORIZON_CHOICES)
    summary = TextField(null=True, blank=True)

    impacts = ManyToManyField('Impact', blank=True, null=True)
    implications = ManyToManyField('Implication', blank=True, null=True)
    indicators = ManyToManyField('Indicator', blank=True, null=True)


class Relation(FiguresMixin, Model):
    draft = BooleanField(default=True)
    assessment = ForeignKey('Assessment', related_name='relations')
    source = ForeignKey('DriverOfChange', related_name='source_relations')
    destination = ForeignKey('GenericElement', related_name='dest_relations', blank=True)
    relationship_type = IntegerField(choices=RELATION_TYPE_CHOICES, null=True, blank=True)
    description = TextField(max_length=2048, null=True, blank=True)

    indicators = ManyToManyField('Indicator', blank=True, null=True)

    def __unicode__(self):
        return u"%s -> %s" % (self.source, self.destination)


class Assessment(Model):
    draft = BooleanField(default=True)
    author_id = CharField(max_length=64)
    title = CharField(max_length=512)
    description = TextField(null=True, blank=True)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)
    geographical_scope = ForeignKey('common.GeographicalScope',
                                    null=True, blank=True)
    country = ForeignKey('common.Country', null=True, blank=True)
    url = CharField(max_length=256, blank=True, null=True)

    class Meta:
        permissions = (
            ('create', 'Create an assessment'),
            ('config', 'Can change configuration'),
        )

    def __unicode__(self):
        return self.title


class Implication(GenericElement, SourcesMixin):
    AREA_POLICY = (
        ('mock_policy', 'Mock policy'),
    )

    policy_area = CharField(
        max_length=64,
        choices=AREA_POLICY,
        default=0,
        blank=True,
        null=True,
    )
    description = TextField(max_length=2048)

    def __unicode__(self):
        return self.name


class Impact(GenericElement, SourcesMixin):
    impact_type = CharField(
        max_length=64,
        choices=IMPACT_TYPES,
        default=0,
        blank=True,
        null=True,
    )

    steep_category = ForeignKey('SteepCategory', related_name='impact_category',
                                blank=True, null=True)
    description = TextField()
