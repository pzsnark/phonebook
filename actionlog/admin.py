from django.contrib import admin

from django.contrib import admin
from .models import ActionLog


# admin.site.register(VisitLog)


@admin.register(ActionLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('ipaddress', 'user', 'http_referer', 'date')
