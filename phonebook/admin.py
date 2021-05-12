from django.contrib import admin
from .models import VisitLog


# admin.site.register(VisitLog)


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('ipaddress', 'http_referer', 'date')
