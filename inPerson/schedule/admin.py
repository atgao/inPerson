from django.contrib import admin
from .models import Section
from .models import RecurrentEvent
from .models import Schedule

admin.site.register(Section)
admin.site.register(RecurrentEvent)
admin.site.register(Schedule)
