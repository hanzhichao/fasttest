from adminsortable.admin import SortableAdmin
from django.contrib import admin
from app.models.module import Module
from app.admin import BaseModelAdmin


@admin.register(Module)
class ModuleAdmin(BaseModelAdmin):
    admin_order = 2
    list_display = ['id', '__str__', 'description']
