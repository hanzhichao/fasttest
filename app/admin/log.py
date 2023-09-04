from django.contrib import admin
from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    该类用于显示 admin 内置的 django_admin_log 表。
    其中，content_type 是指用户修改的 Model 名
    """
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    list_per_page = 25
    readonly_fields = ['action_time', 'user', 'content_type',
                       'object_id', 'object_repr', 'action_flag', 'change_message']
