from django import forms
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from import_export.admin import ImportExportModelAdmin
from prettyjson import PrettyJSONWidget
from simpleui.admin import AjaxAdmin

admin.site.site_header = "FASTTEST"
admin.site.site_title = "FastTest"
admin.site.index_title = "FastTest"


def has_field(obj, field):
    try:
        obj._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False


class BaseTabularInline(admin.TabularInline):
    extra = 0

    formfield_overrides = {
        models.JSONField: {'widget': forms.Textarea(attrs={'rows': '1'})},
        models.TextField: {'widget': forms.Textarea(attrs={'rows': '3'})},
    }


class BaseStackedInline(admin.StackedInline):
    extra = 0

    formfield_overrides = {
        models.JSONField: {'widget': PrettyJSONWidget}
    }


class BaseModelAdmin(AjaxAdmin, ImportExportModelAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['__str__']

    formfield_overrides = {
        models.JSONField: {'widget': PrettyJSONWidget}
    }

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if has_field(obj, 'create_user'):
                obj.create_user = request.user
        if has_field(obj, 'update_user'):
            obj.update_user = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # Include extra css
        }
