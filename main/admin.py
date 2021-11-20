from django.contrib import admin
from .models import Factor, EventSegment, Event, SportSegment, SportKind


admin.site.register(SportKind)
admin.site.register(SportSegment)
admin.site.register(Event)
admin.site.register(EventSegment)
admin.site.register(Factor)
