from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app.admin.base import BaseModelAdmin
from app.models.testrecord import TestRecord

BASE_INLINE_FIELDS = ['testcase', 'status', 'start_time', 'end_time', 'elapsed_time', 'error_msg']
BASE_FIELDS = ['testcase', 'testreport', 'env', 'create_user', 'status', 'start_time', 'end_time']


class TestRecordInline(admin.TabularInline):
    model = TestRecord
    extra = 0
    fields = BASE_INLINE_FIELDS + ['error_reason', 'details']
    readonly_fields = BASE_INLINE_FIELDS + ['details']

    @admin.display(description='详情')
    def details(self, obj):
        html = f'<a href="../../../testrecord/{obj.id}/change">详情</a>'
        return format_html(html)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        if obj and obj.status > 1:
            return True
        return False


@admin.register(TestRecord)
class TestRecordAdmin(BaseModelAdmin):
    admin_order = 6
    list_display = ['id', '__str__', 'env', 'start_time', 'end_time', 'elapsed_time', 'is_success', 'create_user',
                    'error_reason']
    list_filter = ['testcase', 'env', 'create_user', 'error_reason', 'start_time']

    fields = BASE_FIELDS + ['error_reason', 'is_success', 'error_info', 'run_log']
    readonly_fields = BASE_FIELDS + ['is_success', 'error_info', 'run_log']

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        return obj.status == 1

    @admin.display(description='错误信息')
    def error_info(self, obj):
        error_msg = obj.error_msg
        if error_msg:
            try:
                return mark_safe(f'<pre>{error_msg}</pre>')
            except:
                return error_msg
        return '-'

    @admin.display(description='运行日志')
    def run_log(self, obj):
        log = obj.log or ''
        if log:
            try:
                return mark_safe(f'<pre>{obj.log}</pre>')
            except:
                return log
        return '-'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj and obj.status < 2:
            return False
        return True
