from django.contrib import admin

from django.contrib import admin
from .models import ActionLog


# admin.site.register(VisitLog)


@admin.register(ActionLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('ipaddress', 'username', 'path', 'date')
    readonly_fields = ['ipaddress', 'hostname', 'username', 'path', 'date']
