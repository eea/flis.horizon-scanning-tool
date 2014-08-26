from django.contrib import admin
from hstool.models import (
    DriverOfChange, Indicator, Assessment, Relation, EnvironmentalTheme,
    Figure, Source
)


admin.site.register(DriverOfChange)
admin.site.register(Indicator)
admin.site.register(Assessment)
admin.site.register(Relation)
admin.site.register(EnvironmentalTheme)
admin.site.register(Source)
admin.site.register(Figure)
