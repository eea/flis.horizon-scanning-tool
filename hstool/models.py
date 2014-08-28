from django.db.models import (
    Model, CharField, IntegerField, FilePathField, TextField,
    ForeignKey, BooleanField, ManyToManyField)
from hstool.definitions import (
    DOC_TYPE_CHOICES, DOC_TREND_TYPE_CHOICES, DOC_STEEP_CHOICES,
    DOC_TIME_HORIZON_CHOICES, IND_TIMELINE_CHOICES,
    RELATION_TYPE_CHOICES,
)


class EnvironmentalTheme(Model):
    title = CharField(max_length=128)

    class Meta:
        ordering = ('-pk',)

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
    path = FilePathField(max_length=256)


class Source(Model):
    author_id = CharField(max_length=64)
    title = CharField(max_length=512)
    title_original = CharField(max_length=512)
    published_year = IntegerField()
    author = CharField(max_length=512)
    url = CharField(max_length=256)
    path = FilePathField(max_length=256, null=True, blank=True)
    summary = TextField(max_length=2048, null=True, blank=True)


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
        return self.short_name


class DriverOfChange(GenericElement):
    type = IntegerField(choices=DOC_TYPE_CHOICES)
    trend_type = IntegerField(choices=DOC_TREND_TYPE_CHOICES)
    steep_category = CharField(max_length=5, choices=DOC_STEEP_CHOICES)
    time_horizon = IntegerField(choices=DOC_TIME_HORIZON_CHOICES)
    summary = TextField(null=True, blank=True)


class Indicator(GenericElement):
    theme = ForeignKey('EnvironmentalTheme')
    year_base = IntegerField()
    year_end = IntegerField()
    timeline = IntegerField(choices=IND_TIMELINE_CHOICES)


class Relation(Model):
    assessment = ForeignKey('Assessment')
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

    def __unicode__(self):
        return self.title
