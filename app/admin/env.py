from django.contrib import admin

from app.models import Env, EnvVariable
from . import BaseModelAdmin, BaseTabularInline


class EnvVariableInline(BaseTabularInline):
    model = EnvVariable


@admin.register(Env)
class EnvAdmin(BaseModelAdmin):
    pass
