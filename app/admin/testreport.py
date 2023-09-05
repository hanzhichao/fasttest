from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app.admin.base import BaseModelAdmin
from app.models.testreport import TestRecord, TestReport


class TestRecordInline(admin.TabularInline):
    model = TestRecord
    extra = 0
    fields = ['testcase', 'status', 'start_time', 'end_time', 'error_msg', 'details']
    readonly_fields = ['details']

    @admin.display(description='详情')
    def details(self, obj):
        html = f'<a href="../../../testrecord/{obj.id}/change">详情</a>'
        return format_html(html)



@admin.register(TestReport)
class TestReportAdmin(BaseModelAdmin):
    admin_order = 5
    list_display = ['id', '__str__', 'testplan', 'is_success', 'total', 'pass_num', 'pass_rate',
                    'start_time', 'end_time']
    list_display_links = ['__str__']
    list_filter = ['testplan', 'status']
    readonly_fields = ['chart_img']

    list_per_page = 25

    inlines = [TestRecordInline]

    fields = ['testplan', ('status', 'start_time', 'end_time'),
              ('total', 'pass_num', 'fail_num'),
              'chart_img',
              ]

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        return obj.is_success

    @admin.display(description='通过率')
    def pass_rate(self, obj):
        return obj.pass_rate

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description='运行统计')
    def chart_img(self, obj):
        return format_html('<img src="{url}" height="{height}" />'.format(
            url=obj.chart.url,
            height=400,
        ))


@admin.register(TestRecord)
class TestRecordAdmin(BaseModelAdmin):
    admin_order = 6
    list_display = ['id', '__str__', 'start_time', 'end_time', 'is_success']

    list_per_page = 25
    readonly_fields = ['is_success', 'error_info', 'run_log']

    fieldsets = (
        (None, {'fields': ('testcase',
                           'testreport',
                           ('status', 'start_time', 'end_time'),
                           'error_info',
                           'run_log',
                           )}),
        # (None, {'fields': ('run_log',), 'classes': ['collapse']})
    )

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
        return False
