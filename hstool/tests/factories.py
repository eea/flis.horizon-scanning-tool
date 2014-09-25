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


class EnvironmentalThemeFactory(DjangoModelFactory):
    FACTORY_FOR = EnvironmentalTheme


class AssessmentFactory(DjangoModelFactory):
    FACTORY_FOR = Assessment


class DriverFactory(DjangoModelFactory):
    FACTORY_FOR = DriverOfChange
    type = 1
    trend_type = 1
    time_horizon = 1


class IndicatorFactory(DjangoModelFactory):
    FACTORY_FOR = Indicator

    theme = SubFactory(EnvironmentalThemeFactory)
    year_base = 1000
    year_end = 2000
    timeline = 1


class SourceFactory(DjangoModelFactory):
    FACTORY_FOR = Source

    published_year = 1000


class FigureFactory(DjangoModelFactory):
    FACTORY_FOR = Figure

    title = 'figure title'
    file = 'figure file'


class GeoScopeFactory(DjangoModelFactory):
    FACTORY_FOR = GeographicalScope


class CountryFactory(DjangoModelFactory):
    FACTORY_FOR = Country

    iso = 'EN'
    name = 'England'


class RelationFactory(DjangoModelFactory):
    FACTORY_FOR = Relation

    description = 'relation description'
    relationship_type = 1