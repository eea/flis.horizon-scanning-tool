from factory.django import DjangoModelFactory
from factory import SubFactory

from django.contrib.auth.models import User

from hstool.models import (
    Assessment, DriverOfChange, Figure, Indicator, Source, Relation,
    Implication, Impact, SteepCategory, DriverOfChangeType, ImpactType,
    TimeHorizon,
)
from flis_metadata.common.models import (
    Country, EnvironmentalTheme, GeographicalScope
)


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
    username = 'username'


class GeoScopeFactory(DjangoModelFactory):

    class Meta:
        model = GeographicalScope


class CountryFactory(DjangoModelFactory):

    class Meta:
        model = Country

    iso = 'EN'
    name = 'England'


class EnvironmentalThemeFactory(DjangoModelFactory):

    class Meta:
        model = EnvironmentalTheme

    title = 'title'


class SteepCatFactory(DjangoModelFactory):

    class Meta:
        model = SteepCategory

    author_id = 'author_id'
    title = 'Economical'


class DriverTypeFactory(DjangoModelFactory):

    class Meta:
        model = DriverOfChangeType

    author_id = 'author_id'
    title = 'Trends'


class ImpactTypeFactory(DjangoModelFactory):

    class Meta:
        model = ImpactType

    author_id = 'author_id'
    title = 'Risk'


class TimeHorizonFactory(DjangoModelFactory):

    class Meta:
        model = TimeHorizon

    author_id = 'author_id'
    title = '20 years'


class AssessmentFactory(DjangoModelFactory):

    class Meta:
        model = Assessment

    author_id = 'author_id'
    title = 'title'
    description = 'description'


class DriverFactory(DjangoModelFactory):

    class Meta:
        model = DriverOfChange

    author_id = 'author_id'
    short_name = 'short name'
    name = 'long name'
    type = SubFactory(DriverTypeFactory)
    steep_category = SubFactory(SteepCatFactory)
    time_horizon = SubFactory(TimeHorizonFactory)


class SourceFactory(DjangoModelFactory):

    class Meta:
        model = Source

    author_id = 'author_id'
    name = 'title'
    title_original = 'title_original'
    published_year = 1000
    author = 'author'
    url = 'url'
    file = 'file'
    summary = 'summary'


class FigureFactory(DjangoModelFactory):

    class Meta:
        model = Figure

    author_id = 'author_id'
    name = 'name'
    file = 'file'
    theme = SubFactory(EnvironmentalThemeFactory)
    url = 'url'


class RelationFactory(DjangoModelFactory):

    class Meta:
        model = Relation

    description = 'relation description'
    relationship_type = 1


class ImplicationFactory(DjangoModelFactory):

    class Meta:
        model = Implication

    author_id = 'author_id'
    name = 'title'
    description = 'description'


class ImpactFactory(DjangoModelFactory):

    class Meta:
        model = Impact

    short_name = 'short name'
    name = 'long name'
    description = 'description'


class IndicatorFactory(DjangoModelFactory):

    class Meta:
        model = Indicator

    name = 'title'
    theme = SubFactory(EnvironmentalThemeFactory)
    end_date = '2015-11-11'
    start_date = '2015-11-11'
