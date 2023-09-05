from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.utils.html import format_html
from django_cascading_dropdown_widget.widgets import CascadingModelchoices, DjangoCascadingDropdownWidget

from app.admin.base import BaseModelAdmin, BaseTabularInline
from app.models.env import Env
from app.models.testcase import Category, TestCase
from app.models.testplan import TestPlan, TestPlanTestCase
from app.tasks import run_testplan


class TestPlanTestCaseForm(forms.ModelForm):
    class Meta:
        model = TestPlanTestCase
        exclude = []
        widgets = {
            "testcase": DjangoCascadingDropdownWidget(
                choices=CascadingModelchoices(
                    {"model": Category, "related_name": "testcases"},
                    {"model": TestCase, "fk_name": "category"})),
        }


class TestPlanTestCaseInline(BaseTabularInline, SortableTabularInline):
    form = TestPlanTestCaseForm
    model = TestPlanTestCase
    extra = 0


@admin.register(TestPlan)
class TestPlanAdmin(BaseModelAdmin, NonSortableParentAdmin):
    admin_order = 4
    list_display = ['id', 'name', 'description', 'create_user', 'create_time', 'testcase_cnt', 'is_success',
                    'operations']
    list_display_links = ['name']
    exclude = ['create_user', 'update_user', 'last_status']
    list_filter = ['create_user', 'create_time']
    search_fields = ['name']
    # date_hierarchy = 'create_time'

    # filter_horizontal = ['testcases']

    inlines = [TestPlanTestCaseInline]

    actions = ['run', 'copy']

    @admin.display(description='用例数')
    def testcase_cnt(self, obj):
        return obj.testcases.count()

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        status = obj.last_status
        if status:
            return status == 1

    @admin.display(description='操作')
    def operations(self, obj):
        last_result = obj.last_result
        if last_result:
            html = f'<a href="../testreport/{last_result.id}/change">测试报告</a>'
            return format_html(html)
        return ''

    @admin.action(description='复制')
    def copy(self, request, queryset):
        for obj in queryset:
            obj.copy()

    copy.type = 'primary'
    copy.icon = 'el-icon-document'

    @admin.action(description='运行')
    def run(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        env_id = request.POST.get('env')
        if not env_id:
            return JsonResponse(data={'status': 'error', 'msg': '请选择环境'})

        for testplan in queryset:
            run_testplan(testplan.id, env_id)

        return JsonResponse(data={'status': 'success', 'msg': '运行成功'})

    run.type = 'success'
    run.icon = 'el-icon-arrow-right'
    run.layer = {
        'title': '选择测试环境',
        'confirm_button': '确认',
        'width': '35%',
        'params': [{
            'label': '测试环境',
            'width': '200px',
            'key': 'env',
            'type': 'select',
            'options': [{'key': env.id, 'label': env.name} for env in Env.objects.all()]
        }]
    }
