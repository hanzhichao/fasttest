from django.contrib import admin

from app.models.env import Env, EnvVariable, LibraryConfig
from .base import BaseModelAdmin, BaseStackedInline, BaseTabularInline


class EnvVariableInline(BaseTabularInline):
    model = EnvVariable


class LibraryConfigInline(BaseStackedInline):
    model = LibraryConfig


@admin.register(Env)
class EnvAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']
    admin_order = 1

    inlines = [LibraryConfigInline, EnvVariableInline]
