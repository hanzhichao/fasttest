from django.contrib import admin

from app.admin.base import BaseModelAdmin, BaseTabularInline
from app.models.library import Library, Method


class MethodInline(BaseTabularInline):
    model = Method


@admin.register(Library)
class LibraryAdmin(BaseModelAdmin):
    admin_order = 7
    list_display = ['id', 'name', 'description', 'methods_cnt']
    list_display_links = ['name']

    inlines = [MethodInline]

    @admin.display(description='方法数量')
    def methods_cnt(self, obj):
        return obj.methods.count()
