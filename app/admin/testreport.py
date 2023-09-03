from django.contrib import admin

from app.admin.base import BaseModelAdmin
from app.models import TestRecord, TestReport


class TestRecordInline(admin.TabularInline):
    model = TestRecord
    extra = 0
    fields = ['testcase', 'status', 'start_time', 'end_time']
    readonly_fields = ['testcase', 'status', 'start_time', 'end_time']

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TestReport)
class TestReportAdmin(BaseModelAdmin):

    list_display = ['id', '__str__', 'testplan', 'is_success', 'total', 'pass_num', 'pass_rate',
                    'start_time', 'end_time']
    list_display_links = ['__str__']
    list_filter = ['testplan', 'status']

    inlines = [TestRecordInline]

    fields = ['testplan', 'status', ('start_time', 'end_time'),
              ('total', 'pass_num', 'fail_num')]
    readonly_fields = ['testplan', 'status', 'start_time', 'end_time', 'total',
                       'pass_num', 'fail_num']

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
