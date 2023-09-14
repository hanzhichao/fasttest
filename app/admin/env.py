from attachments.models import Attachment
from attachments.models import Attachment
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from app.models.env import Env, EnvVariable, LibraryConfig
from .base import BaseModelAdmin, BaseStackedInline, BaseTabularInline


class EnvVariableInline(BaseTabularInline):
    model = EnvVariable


class LibraryConfigInline(BaseStackedInline):
    model = LibraryConfig


class AttachmentInline(GenericTabularInline):
    model = Attachment
    exclude = ('creator',)
    extra = 0


@admin.register(Env)
class EnvAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']
    admin_order = 1

    inlines = [LibraryConfigInline, EnvVariableInline, AttachmentInline]
