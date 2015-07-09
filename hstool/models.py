from datetime import datetime
from django.db.models import (
    Model, CharField, IntegerField, TextField, ForeignKey, BooleanField,
    ManyToManyField, FileField,
    DateTimeField)
from django.forms.forms import ValidationError
from django.conf import settings

from hstool.definitions import (
    DOC_TYPE_CHOICES, DOC_TREND_TYPE_CHOICES, DOC_STEEP_CHOICES,
    DOC_TIME_HORIZON_CHOICES,
    RELATION_TYPE_CHOICES, DOC_UNCERTAINTIES_TYPE_CHOICES,
    IMPACT_TYPES,
)
from hstool.utils import path_and_rename_sources, path_and_rename_figures


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


class Source(Model):
    draft = BooleanField(default=True)
    author_id = CharField(max_length=64)
    title = CharField(max_length=512)
    title_original = CharField(max_length=512)
    published_year = IntegerField()
    author = CharField(max_length=512)
    url = CharField(max_length=256)
    file = FileField(upload_to=path_and_rename_sources)
    summary = TextField(max_length=2048)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

    def __unicode__(self):
        return self.title


class GenericElement(Model):
    draft = BooleanField(default=True)
    author_id = CharField(max_length=64)
    short_name = CharField(max_length=64)
    name = CharField(max_length=255)
    geographical_scope = ForeignKey('common.GeographicalScope',
                                    null=True, blank=True)
    country = ForeignKey('common.Country', null=True, blank=True)
    url = CharField(max_length=256, blank=True, null=True)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

    sources = ManyToManyField('Source', blank=True, null=True)

    def is_figureindicator(self):
        try:
            if self.figureindicator:
                return True
        except FigureIndicator.DoesNotExist:
            return False
        return False

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


class FigureIndicator(GenericElement):
    is_indicator = BooleanField(default=False)
    file = ContentTypeRestrictedFileField(
        upload_to=path_and_rename_figures,
        content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES,
    )
    theme = ForeignKey('common.EnvironmentalTheme')


class DriverOfChange(GenericElement):
    type = IntegerField(choices=DOC_TYPE_CHOICES)
    trend_type = IntegerField(choices=DOC_TREND_TYPE_CHOICES,
                              default=1)
    uncertainty_type = IntegerField(choices=DOC_UNCERTAINTIES_TYPE_CHOICES,
                                    default=1)
    steep_category = CharField(max_length=5, choices=DOC_STEEP_CHOICES)
    time_horizon = IntegerField(choices=DOC_TIME_HORIZON_CHOICES)
    summary = TextField(null=True, blank=True)

    figureindicators = ManyToManyField('FigureIndicator', blank=True, null=True)
    impacts = ManyToManyField('Impact', blank=True, null=True)
    implications = ManyToManyField('Implication', blank=True, null=True)


class Relation(Model):
    draft = BooleanField(default=True)
    assessment = ForeignKey('Assessment', related_name='relations')
    source = ForeignKey('DriverOfChange', related_name='source_relations')
    destination = ForeignKey('GenericElement', related_name='dest_relations', blank=True)
    relationship_type = IntegerField(choices=RELATION_TYPE_CHOICES, null=True, blank=True)
    description = TextField(max_length=2048, null=True, blank=True)

    figureindicators = ManyToManyField('FigureIndicator', blank=True, null=True)

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


class Implication(GenericElement):
    AREA_POLICY = (
        ('mock_policy', 'Mock policy'),
    )

    title = CharField(max_length=512)
    policy_area = CharField(
        max_length=64,
        choices=AREA_POLICY,
        default=0,
        blank=True,
        null=True,
    )
    description = TextField(max_length=2048)

    figureindicators = ManyToManyField('FigureIndicator', blank=True, null=True)

    def __unicode__(self):
        return self.title


class Impact(GenericElement):
    impact_type = CharField(
        max_length=64,
        choices=IMPACT_TYPES,
        default=0,
        blank=True,
        null=True,
    )

    steep_category = CharField(
        max_length=64,
        choices=DOC_STEEP_CHOICES,
        default=0,
        blank=True,
        null=True,
    )

    description = TextField()

    figureindicators = ManyToManyField('FigureIndicator', blank=True, null=True)
