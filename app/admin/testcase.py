
from adminsortable.admin import NonSortableParentAdmin
from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.utils.html import format_html
from django_object_actions import takes_instance_or_queryset
from import_export import resources, widgets
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from taggit.forms import TagField, TagWidget

from app.admin.base import BaseModelAdmin, ChoicesWidget, action, create_select_layer
from app.admin.step import SetupStepInline, TeardownStepInline, TestStepInline
from app.models.base import PRIORITY_CHOICES
from app.models.env import Env
from app.models.step import TestStep
from app.models.testcase import TestCase
from app.models.testplan import TestPlan, TestPlanTestCase
from app.tasks import run_testcase, run_testcase_task
from app.utils import get_celery_worker_status


class TestCaseResource(resources.ModelResource):
    id = Field(attribute='id', column_name='用例ID')
    name = Field(attribute='name', column_name='用例名称')
    description = Field(attribute='description', column_name='用例描述')
    category = Field(attribute='category__name', column_name='分类名称')
    priority = Field(attribute='priority',
                     widget=ChoicesWidget(PRIORITY_CHOICES),
                     column_name='优先级')
    setups = Field(
        column_name='预置条件',
        attribute='setup_steps',
        widget=widgets.ManyToManyWidget(TestStep, field='name', separator='\n')
    )
    steps = Field(
        column_name='测试步骤',
        attribute='test_steps',
        widget=widgets.ManyToManyWidget(TestStep, field='name', separator='\n')
    )
    teardowns = Field(
        column_name='测试清理',
        attribute='teardown_steps',
        widget=widgets.ManyToManyWidget(TestStep, field='name', separator='\n')
    )

    tags = Field(
        column_name='标签',
        attribute='tags',
        widget=widgets.ManyToManyWidget(TestStep, field='name', separator=', ')
    )
    create_user = Field(attribute='create_user__username', column_name='创建人')
    create_time = Field(attribute='create_time', column_name='创建时间', widget=DateTimeWidget('%Y-%m-%d %H:%M:%S'))
    update_user = Field(attribute='update_user__username', column_name='更新人')
    update_time = Field(attribute='update_time', column_name='更新时间', widget=DateTimeWidget('%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = TestCase
        # fields = ('name', 'category_name', 'priority', 'description', 'create_user__username', 'all_steps')


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
    resource_class = TestCaseResource
    # 列表页配置
    list_display = ['id', 'name', 'category', 'priority', 'tag_list', 'is_success', 'test_steps_cnt', 'results_cnt',
                    'operations']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['category', 'priority', 'tags', 'create_user', 'create_time']
    autocomplete_fields = ['resources']
    actions = ['copy', 'run', 'create_testplan']
    change_actions = ['run']


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

    @action(description='复制', type='primary', icon='el-icon-document')
    def copy(self, request, queryset):
        for obj in queryset:
            obj.copy()

    @action(description='运行', type='success', icon='el-icon-arrow-right',
            layer=create_select_layer(label='测试环境', key='env', model=Env))
    @takes_instance_or_queryset
    def run(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        env_id = request.POST.get('env')
        if not env_id:
            return JsonResponse(data={'status': 'error', 'msg': '请选择环境'})

        celery_worker_status = get_celery_worker_status()
        if celery_worker_status is None:
            env = Env.objects.get(id=env_id)
            for testcase in queryset:
                run_testcase(testcase, env, request.user.id)
        else:
            for testcase in queryset:
                run_testcase_task.delay(testcase.id, env_id, request.user.id)

        return JsonResponse(data={'status': 'success', 'msg': '运行成功'})

    @action(description='创建测试计划', type='success', icon='el-icon-document')
    def create_testplan(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        name = request.POST.get('testplan_name')
        description = request.POST.get('testplan_description') or ''
        if not name:
            return JsonResponse(data={'status': 'error', 'msg': '请选输入测试计划名称'})

        testplan = TestPlan.objects.create(name=name,
                                           description=description,
                                           create_user=request.user,
                                           update_user=request.user)
        for index, testcase in enumerate(queryset):
            TestPlanTestCase.objects.create(
                testplan=testplan,
                testcase=testcase,
                order=index + 1
            )

        return JsonResponse(data={'status': 'success', 'msg': f'创建测试计划{testplan.id}成功'})

    create_testplan.layer = {
        'title': '创建测试计划',
        'width': '35%',
        'params': [
            {
                'type': 'input',
                'width': '300px',
                'key': 'testplan_name',
                'label': '名称',
                'require': True,
            },
            {
                'type': 'textarea',
                'width': '300px',
                'key': 'testplan_description',
                'label': '描述',
            },
        ]
    }
