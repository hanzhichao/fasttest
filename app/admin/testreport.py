from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_object_actions import action

from app.admin.base import BaseModelAdmin
from app.admin.testrecord import TestRecordInline
from app.models.testreport import TestReport


@admin.register(TestReport)
class TestReportAdmin(BaseModelAdmin):
    admin_order = 5
    list_display = ['id', '__str__', 'testplan', 'env', 'is_success', 'total', 'pass_num',
                    'pase_rate_progress',
                    'start_time', 'end_time', 'elapsed_time', 'create_user']
    list_display_links = ['__str__']
    list_filter = ['testplan', 'env', 'create_user', 'start_time']
    readonly_fields = ['testplan', 'env', 'create_user', 'status', 'start_time', 'end_time', 'total', 'pass_num',
                       'fail_num',
                       'chart_img']

    inlines = [TestRecordInline]

    fields = ['testplan',
              'env',
              'create_user',
              ('status', 'start_time', 'end_time'),
              ('total', 'pass_num', 'fail_num'),
              'chart_img',
              ]

    change_actions = ('download_report',)

    @action(label="下载", description="下载测试报告")  # optional
    def download_report(self, request, obj):
        print('下载', obj)

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        return obj.is_success

    @admin.display(description='通过率')
    def pass_rate(self, obj):
        return obj.pass_rate

    @admin.display(description='通过率')
    def pase_rate_progress(self, obj):
        pass_rate = obj.pass_rate or '0%'
        bg_color = 'rgb(235, 238, 245)'
        text_color = 'rgb(255, 255, 255)'
        print(pass_rate)
        if pass_rate == '0%':
            text_color = 'rgb(96, 98, 102)'

        if pass_rate == '100.0%':
            type = 'is-success'
        else:
            type = 'is-warning'

        html = f'''<div role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" class="el-progress el-progress--line {type} el-progress--text-inside">
        <div class="el-progress-bar">
        <div class="el-progress-bar__outer" style="height: 24px; background-color: {bg_color};">
        <div class="el-progress-bar__inner" style="width: {pass_rate};">
        <div class="el-progress-bar__innerText" style="color: {text_color};">{pass_rate}</div>
        </div></div></div><!----></div>
        '''
        return mark_safe(html)

    def has_add_permission(self, request):
        return False


    @admin.display(description='运行统计')
    def chart_img(self, obj):
        chart = obj.get_chart()
        return format_html('<img src="{url}" height="{height}" />'.format(
            url=chart.url,
            height=400,
        ))
