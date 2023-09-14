from django.contrib import admin

from app.admin.base import BaseModelAdmin
from app.models.resource import Resource


@admin.register(Resource)
class ResourceAdmin(BaseModelAdmin):
    admin_order = 8
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']
    search_fields = ['name']
