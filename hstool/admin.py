from django.contrib import admin
from hstool.models import (
    DriverOfChange, Indicator, Assessment, Relation, Figure, Source
)
from flis_metadata.common.models import (
    Country, GeographicalScope, EnvironmentalTheme
)


admin.site.register(DriverOfChange)
admin.site.register(Indicator)
admin.site.register(Assessment)
admin.site.register(Relation)
admin.site.register(Source)
admin.site.register(Figure)
admin.site.register(Country)
admin.site.register(GeographicalScope)
admin.site.register(EnvironmentalTheme)
