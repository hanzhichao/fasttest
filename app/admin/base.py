from django import forms
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django_object_actions import DjangoObjectActions
from import_export.admin import ImportExportActionModelAdmin
from prettyjson import PrettyJSONWidget
from simpleui.admin import AjaxAdmin

from fasttest import settings

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


class BaseModelAdmin(DjangoObjectActions, ImportExportActionModelAdmin, AjaxAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['__str__']

    list_per_page = settings.LIST_PER_PAGE

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

    def save_formset(self, request, form, formset, change):
        objs = formset.save(commit=False)
        for obj in objs:
            try:
                if not obj.pk and obj.has_field('creator'):
                    obj.creator = request.user

                if obj.has_field('operator'):
                    obj.operator = request.user
            except Exception:
                pass

            obj.save()
        formset.save_m2m()

    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # Include extra css
        }


def create_select_layer(label, key, model, label_field='name'):
    return {
        'title': f'选择{label}',
        'width': '35%',
        'params': [{
            'label': label,
            'width': '200px',
            'key': key,
            'type': 'select',
            'options': [{'key': obj.id, 'label': getattr(obj, label_field)}
                        for obj in model.objects.all()]
        }]
    }


def action(function=None, *, permissions=None, description=None,
           type=None, icon=None, layer=None):
    def decorator(func):
        if permissions is not None:
            func.allowed_permissions = permissions
        if description is not None:
            func.short_description = description
        if type is not None:
            func.type = type
        if icon is not None:
            func.icon = icon
        if layer is not None:
            func.layer = layer
        return func

    if function is None:
        return decorator
    else:
        return decorator(function)


from import_export.widgets import Widget


class ChoicesWidget(Widget):
    """
    Widget that uses choice display values in place of database values
    """

    def __init__(self, choices, *args, **kwargs):
        """
        Creates a self.choices dict with a key, display value, and value,
        db value, e.g. {'Chocolate': 'CHOC'}
        """
        self.choices = dict(choices)
        self.revert_choices = dict((v, k) for k, v in self.choices.items())

    def clean(self, value, row=None, *args, **kwargs):
        """Returns the db value given the display value"""
        return self.revert_choices.get(value, value) if value else None

    def render(self, value, obj=None):
        """Returns the display value given the db value"""
        return self.choices.get(value, '')
