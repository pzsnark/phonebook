from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin

from . import forms
from .models import Entry, Company
from .forms import EntryForm


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    form = EntryForm
    list_display = (
        'displayName', 'title', 'physicalDeliveryOfficeName', 'telephoneNumber', 'mobile', 'mail', 'company'
    )


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ('name',)
