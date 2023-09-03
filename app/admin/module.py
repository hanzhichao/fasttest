from django.contrib import admin
from app.models import Module
from app.admin import BaseModelAdmin


@admin.register(Module)
class ModuleAdmin(BaseModelAdmin):
    pass
