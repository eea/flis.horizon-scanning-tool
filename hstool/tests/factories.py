from factory.django import DjangoModelFactory
from factory import SubFactory

from django.contrib.auth.models import User

from hstool.models import (
    Assessment, DriverOfChange, FigureIndicator, Source, Relation,
    Implication, Impact,
)
from flis_metadata.common.models import (
    Country, EnvironmentalTheme, GeographicalScope
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

    title = 'title'


class AssessmentFactory(DjangoModelFactory):
    FACTORY_FOR = Assessment

    author_id = 'author_id'
    title = 'title'
    description = 'description'


class DriverFactory(DjangoModelFactory):
    FACTORY_FOR = DriverOfChange

    author_id = 'author_id'
    short_name = 'short name'
    name = 'long name'
    type = 1
    trend_type = 1
    steep_category = 'P'
    time_horizon = 1


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


class FigureFactory(DjangoModelFactory):
    FACTORY_FOR = FigureIndicator

    author_id = 'author_id'
    is_indicator = 'yes'
    title = 'title'
    file = 'file'
    theme = SubFactory(EnvironmentalThemeFactory)
    url = 'url'

class RelationFactory(DjangoModelFactory):
    FACTORY_FOR = Relation

    description = 'relation description'
    relationship_type = 1


class ImplicationFactory(DjangoModelFactory):
    FACTORY_FOR = Implication

    author_id = 'author_id'
    title = 'title'
    description = 'description'


class ImpactFactory(DjangoModelFactory):
    FACTORY_FOR = Impact

    short_name = 'short name'
    name = 'long name'
    description = 'description'
