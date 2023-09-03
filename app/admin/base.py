from django import forms
from django.contrib import admin
from django.db import models
from simpleui.admin import AjaxAdmin
from import_export.admin import ImportExportModelAdmin


class BaseTabularInline(admin.TabularInline):
    extra = 0

    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': '1'})}
    }


class BaseModelAdmin(AjaxAdmin, ImportExportModelAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['__str__']

