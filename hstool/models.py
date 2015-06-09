from datetime import datetime
from django.db.models import (
    Model, CharField, IntegerField, TextField, ForeignKey, BooleanField,
    ManyToManyField, FileField,
    DateTimeField)
from django.forms.forms import ValidationError
from django.conf import settings

from hstool.definitions import (
    DOC_TYPE_CHOICES, DOC_TREND_TYPE_CHOICES, DOC_STEEP_CHOICES,
    DOC_TIME_HORIZON_CHOICES, IND_TIMELINE_CHOICES,
    RELATION_TYPE_CHOICES, DOC_UNCERTAINTIES_TYPE_CHOICES,
)
from hstool.utils import path_and_rename


class ContentTypeRestrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")

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


class Figure(Model):
    author_id = CharField(max_length=64)
    title = CharField(max_length=512, default='')
    file = ContentTypeRestrictedFileField(
        upload_to=path_and_rename('files/figures'),
        content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES,
    )
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

    def __unicode__(self):
        return self.title


class Source(Model):
    author_id = CharField(max_length=64)
    title = CharField(max_length=512)
    title_original = CharField(max_length=512)
    published_year = IntegerField()
    author = CharField(max_length=512)
    url = CharField(max_length=256)
    file = FileField(upload_to=path_and_rename('files/sources'))
    summary = TextField(max_length=2048)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

    def __unicode__(self):
        return self.title


class GenericElement(Model):
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
    figures = ManyToManyField('Figure', blank=True, null=True)

    def __unicode__(self):
        return self.name


class DriverOfChange(GenericElement):
    type = IntegerField(choices=DOC_TYPE_CHOICES)
    trend_type = IntegerField(choices=DOC_TREND_TYPE_CHOICES,
                              default=1)
    uncertainty_type = IntegerField(choices=DOC_UNCERTAINTIES_TYPE_CHOICES,
                                    default=1)
    steep_category = CharField(max_length=5, choices=DOC_STEEP_CHOICES)
    time_horizon = IntegerField(choices=DOC_TIME_HORIZON_CHOICES)
    summary = TextField(null=True, blank=True)

    def __unicode__(self):
        return '{0}: {1} - {2} - {3} - {4}'.format(
            self.name,
            dict(DOC_TYPE_CHOICES).get(self.type, ''),
            dict(DOC_TREND_TYPE_CHOICES).get(self.trend_type, ''),
            dict(DOC_STEEP_CHOICES).get(self.steep_category, ''),
            dict(DOC_TIME_HORIZON_CHOICES).get(self.time_horizon, ''),
        )


class Indicator(GenericElement):
    theme = ForeignKey('common.EnvironmentalTheme')
    year_base = IntegerField()
    year_end = IntegerField()
    timeline = IntegerField(choices=IND_TIMELINE_CHOICES)

    def __unicode__(self):
        return '{0}: {1} - {2} - {3} - {4}'.format(
            self.name,
            self.theme, self.year_base, self.year_end,
            dict(IND_TIMELINE_CHOICES).get(self.timeline, ''),
        )


class Relation(Model):
    assessment = ForeignKey('Assessment', related_name='relations')
    source = ForeignKey('GenericElement', related_name='source_relations')
    destination = ForeignKey('GenericElement', related_name='dest_relations')
    relationship_type = IntegerField(choices=RELATION_TYPE_CHOICES)
    description = TextField(max_length=2048)

    figures = ManyToManyField('Figure', blank=True, null=True)

    def __unicode__(self):
        return u"%s -> %s" % (self.source, self.destination)


class Assessment(Model):
    author_id = CharField(max_length=64)
    title = CharField(max_length=512)
    description = TextField(null=True, blank=True)
    added = DateTimeField(auto_now_add=True, editable=False,
                          default=datetime.now)

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
        choices= AREA_POLICY,
        default=0,
        blank=True,
        null=True,
    )
    description = TextField(max_length=2048)

    def __unicode__(self):
        return self.title
