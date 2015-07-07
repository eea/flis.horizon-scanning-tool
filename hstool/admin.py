from django.contrib import admin
from hstool.models import (
    DriverOfChange, Assessment, Relation, FigureIndicator, Source
)
from flis_metadata.common.models import (
    Country, GeographicalScope, EnvironmentalTheme
)


admin.site.register(DriverOfChange)
admin.site.register(Assessment)
admin.site.register(Relation)
admin.site.register(Source)
admin.site.register(FigureIndicator)
admin.site.register(Country)
admin.site.register(GeographicalScope)
admin.site.register(EnvironmentalTheme)
