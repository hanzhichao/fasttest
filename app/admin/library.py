from django.contrib import admin

from app.admin.base import BaseModelAdmin
from app.models import Library, Method


class MethodInline(admin.TabularInline):
    model = Method
    extra = 0


@admin.register(Library)
class LibraryAdmin(BaseModelAdmin):
    inlines = [MethodInline]
