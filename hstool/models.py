from django.db.models import (
    Model, CharField, IntegerField, TextField, ForeignKey, BooleanField,
    ManyToManyField, FileField,
)
from django.forms.forms import ValidationError
from django.conf import settings

from hstool.definitions import (
    DOC_TYPE_CHOICES, DOC_TREND_TYPE_CHOICES, DOC_STEEP_CHOICES,
    DOC_TIME_HORIZON_CHOICES, IND_TIMELINE_CHOICES,
    RELATION_TYPE_CHOICES,
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

            types = ', '.join(map(_get_extension, self.content_types))
            raise ValidationError(
                'File type not supported: {0}. Please upload only {1}.'
                .format(content_type, types))

        return data

    def south_field_triple(self):
        return (
            'hstool.ContentTypeRestrictedFileField',
            [],
            dict(upload_to=path_and_rename('files/figures'),
                 content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES)
        )


class EnvironmentalTheme(Model):
    title = CharField(max_length=128)

    class Meta:
        ordering = ('-pk',)
        permissions = (
            ('config', 'Can change configuration'),
        )

    def __unicode__(self):
        return self.title


class GeographicalScope(Model):
    title = CharField(max_length=128)
    require_country = BooleanField(default=False)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return self.title


class Country(Model):
    iso = CharField(max_length=2, primary_key=True)
    name = CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Figure(Model):
    author_id = CharField(max_length=64)
    title = CharField(max_length=512, default='')
    file = ContentTypeRestrictedFileField(
        upload_to=path_and_rename('files/figures'),
        content_types=settings.SUPPORTED_FILES_FACTS_AND_FIGURES,
    )

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

    def __unicode__(self):
        return self.title


class GenericElement(Model):
    author_id = CharField(max_length=64)
    short_name = CharField(max_length=64)
    name = CharField(max_length=255)
    geographical_scope = ForeignKey('GeographicalScope', null=True, blank=True)
    country = ForeignKey('Country', null=True, blank=True)
    url = CharField(max_length=256, blank=True, null=True)

    sources = ManyToManyField('Source', blank=True, null=True)
    figures = ManyToManyField('Figure', blank=True, null=True)

    def __unicode__(self):
        return self.name


class DriverOfChange(GenericElement):
    type = IntegerField(choices=DOC_TYPE_CHOICES)
    trend_type = IntegerField(choices=DOC_TREND_TYPE_CHOICES)
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
    theme = ForeignKey('EnvironmentalTheme')
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

    class Meta:
        permissions = (
            ('create', 'Create an assessment'),
        )

    def __unicode__(self):
        return self.title
