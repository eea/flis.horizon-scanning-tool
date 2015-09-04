from factory.django import DjangoModelFactory
from factory import SubFactory
from datetime import  date

from django.contrib.auth.models import User

from hstool.models import (
    Assessment, DriverOfChange, Figure, Indicator, Source, Relation,
    Implication, Impact, SteepCategory, DriverOfChangeType, ImpactType, TimeHorizon
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


class SteepCatFactory(DjangoModelFactory):
    FACTORY_FOR = SteepCategory

    author_id = 'author_id'
    title = 'Economical'


class DriverTypeFactory(DjangoModelFactory):
    FACTORY_FOR = DriverOfChangeType

    author_id = 'author_id'
    title = 'Trends'


class ImpactTypeFactory(DjangoModelFactory):
    FACTORY_FOR = ImpactType

    author_id = 'author_id'
    title = 'Risk'


class TimeHorizonFactory(DjangoModelFactory):
    FACTORY_FOR = TimeHorizon

    author_id = 'author_id'
    title = '20 years'


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
    type = SubFactory(DriverTypeFactory)
    steep_category = SubFactory(SteepCatFactory)
    time_horizon = SubFactory(TimeHorizonFactory)


class SourceFactory(DjangoModelFactory):
    FACTORY_FOR = Source

    author_id = 'author_id'
    name = 'title'
    title_original = 'title_original'
    published_year = 1000
    author = 'author'
    url = 'url'
    file = 'file'
    summary = 'summary'


class FigureFactory(DjangoModelFactory):
    FACTORY_FOR = Figure

    author_id = 'author_id'
    name = 'name'
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
    name = 'title'
    description = 'description'


class ImpactFactory(DjangoModelFactory):
    FACTORY_FOR = Impact

    short_name = 'short name'
    name = 'long name'
    description = 'description'


class IndicatorFactory(DjangoModelFactory):
    FACTORY_FOR = Indicator

    name = 'title'
    theme = SubFactory(EnvironmentalThemeFactory)
    end_date = '2015-11-11'
    start_date = '2015-11-11'
