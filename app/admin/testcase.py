from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html
from django_cascading_dropdown_widget.widgets import CascadingModelchoices, DjangoCascadingDropdownWidget
from taggit.forms import TagField, TagWidget

from app.admin.base import BaseModelAdmin, BaseTabularInline
from app.models.env import Env
from app.models.library import Library, Method
from app.models.step import SetupStep, Step, TeardownStep, TestStep
from app.models.testcase import Category, TestCase
from app.tasks import run_testcase


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = []
        widgets = {
            "method": DjangoCascadingDropdownWidget(
                choices=CascadingModelchoices(
                    {"model": Library, "related_name": "methods"},
                    {"model": Method, "fk_name": "library"})),
        }


class TestStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = TestStep
    exclude = ['type', 'order']


class SetupStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = SetupStep
    exclude = ['type', 'order']


class TeardownStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = TeardownStep
    exclude = ['type', 'order']


class TestCaseModelForm(forms.ModelForm):
    tags = TagField(label='标签', required=False, widget=TagWidget(attrs={'class': 'vTextField'}))
    description = forms.CharField(label='描述', required=False,
                                  widget=forms.Textarea(attrs={'class': 'vTextField', 'rows': '3'}))

    class Meta:
        model = TestCase
        exclude = ['create_user', 'update_user', 'last_status', 'last_result', 'order']



@admin.register(TestCase)
class TestCaseAdmin(BaseModelAdmin, NonSortableParentAdmin):
    admin_order = 3
    # 列表页配置
    list_display = ['id', 'name', 'category', 'priority', 'tag_list', 'create_time', 'create_user', 'is_success',
                    'operations']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['category', 'priority', 'tags', 'create_user', 'create_time']
    actions = ['run', 'copy']

    # 修改页配置
    inlines = [SetupStepInline, TestStepInline, TeardownStepInline]
    form = TestCaseModelForm

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        status = obj.last_status
        if status:
            return status == 1

    @admin.display(description='标签')
    def tag_list(self, obj):
        return format_html(' '.join([
            f'<span class="el-tag el-tag--small el-tag--light">{tag.name}</span>'
            for tag in obj.tags.all()]))

    @admin.display(description='操作')
    def operations(self, obj):
        last_result = obj.last_result
        if last_result:
            html = f'<a href="../testrecord/{last_result.id}/change">运行详情</a>'
            return format_html(html)
        return ''

    def operation_run(self, result, testcase_id):
        testcase = TestCase.objects.get(id=testcase_id)
        pass

    def operation_view_log(self, result, testcase_id):
        pass

    @admin.action(description='复制')
    def copy(self, request, queryset):
        for obj in queryset:
            obj.copy()

    copy.type = 'primary'
    copy.icon = 'el-icon-document'

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path('<testcase_id>/run', self.operation_run),
            path('<testcase_id>/view_log', self.operation_view_log)
        ]
        return extra_urls + urls

    @admin.action(description='运行')
    def run(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        env_id = request.POST.get('env')
        if not env_id:
            return JsonResponse(data={'status': 'error', 'msg': '请选择环境'})
        # env = Env.objects.get(id=env_id)

        for testcase in queryset:
            run_testcase(testcase.id, env_id)

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
