from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin

from .models import Entry, Company


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('sn', 'givenName', 'middle_name', 'displayName', 'telephoneNumber', 'mobile', 'mail')
    # readonly_fields = ('')


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
