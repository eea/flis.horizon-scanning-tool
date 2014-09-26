from factory.django import DjangoModelFactory
from factory import SubFactory

from django.contrib.auth.models import User

from hstool.models import (
    Assessment, DriverOfChange, Indicator, Source, Figure, EnvironmentalTheme,
    GeographicalScope, Country, Relation,
)


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User

    username = 'username'


class GeoScopeFactory(DjangoModelFactory):
    FACTORY_FOR = GeographicalScope


class CountryFactory(DjangoModelFactory):
    FACTORY_FOR = Country

    iso = 'EN'
    name = 'England'


class EnvironmentalThemeFactory(DjangoModelFactory):
    FACTORY_FOR = EnvironmentalTheme


class AssessmentFactory(DjangoModelFactory):
    FACTORY_FOR = Assessment


class DriverFactory(DjangoModelFactory):
    FACTORY_FOR = DriverOfChange

    author_id = 'author_id'
    short_name = 'short name'
    name = 'long name'
    type = 1
    trend_type = 1
    steep_category = 'P'
    time_horizon = 1


class IndicatorFactory(DjangoModelFactory):
    FACTORY_FOR = Indicator

    theme = SubFactory(EnvironmentalThemeFactory)
    year_base = 1000
    year_end = 2000
    timeline = 1


class SourceFactory(DjangoModelFactory):
    FACTORY_FOR = Source

    author_id = 'author_id'
    title = 'title'
    title_original = 'title_original'
    published_year = 1000
    author = 'author'
    url = 'url'
    file = 'file'
    summary = 'summary'
    country = SubFactory(CountryFactory)


class FigureFactory(DjangoModelFactory):
    FACTORY_FOR = Figure

    title = 'figure title'
    file = 'figure file'


class RelationFactory(DjangoModelFactory):
    FACTORY_FOR = Relation

    description = 'relation description'
    relationship_type = 1