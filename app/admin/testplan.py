from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_cascading_dropdown_widget.widgets import CascadingModelchoices, DjangoCascadingDropdownWidget
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from app.admin.base import BaseModelAdmin, BaseTabularInline, action, create_select_layer
from app.models.env import Env
from app.models.testcase import Category, TestCase
from app.models.testplan import TestPlan, TestPlanTestCase
from app.runner import run_testplan
from app.tasks import run_testplan_task
from app.utils import get_celery_worker_status


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
    list_display = ['id', 'name', 'description', 'testcase_cnt', 'results_cnt', 'is_success', 'periodic_task',
                    'periodic_task_enabled',
                    'operations']
    list_display_links = ['name']
    exclude = ['create_user', 'update_user', 'last_status']
    list_filter = ['create_user', 'create_time']
    search_fields = ['name']

    inlines = [TestPlanTestCaseInline]

    actions = ['copy', 'run', 'add_periodic_task', 'enable_task', 'disable_task', ]

    @admin.display(description='运行状态', boolean=True)
    def is_success(self, obj):
        status = obj.last_status
        if status:
            return status == 1



    @admin.display(description='定时任务启动', boolean=True)
    def periodic_task_enabled(self, obj):

        if obj.periodic_task:
            return obj.periodic_task.enabled

    @admin.display(description='操作')
    def operations(self, obj):
        last_result = obj.last_result
        if last_result:
            html = f'<a href="../testreport/{last_result.id}/change">测试报告</a>'
            return format_html(html)
        return ''

    @action(description='复制', type='primary', icon='el-icon-document')
    def copy(self, request, queryset):
        for obj in queryset:
            obj.copy()

    @action(description='启动定时任务', type='success')
    def enable_task(self, request, queryset):
        for obj in queryset:
            if obj.periodic_task:
                obj.periodic_task.enabled = True
                obj.periodic_task.save()

    @action(description='停止定时任务', type='warning')
    def disable_task(self, request, queryset):
        for obj in queryset:
            if obj.periodic_task:
                obj.periodic_task.enabled = False
                obj.periodic_task.save()

    @action(description='运行', type='success', icon='el-icon-arrow-right',
            layer=create_select_layer(label='测试环境', key='env', model=Env))
    def run(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        env_id = request.POST.get('env')
        if not env_id:
            return JsonResponse(data={'status': 'error', 'msg': '请选择环境'})

        celery_worker_status = get_celery_worker_status()
        if celery_worker_status is None:
            env = Env.objects.get(id=env_id)
            for testplan in queryset:
                run_testplan(testplan, env, request.user.id)
        else:
            for testplan in queryset:
                run_testplan_task.delay(testplan.id, env_id, request.user.id)

        return JsonResponse(data={'status': 'success', 'msg': '运行成功'})

    @action(description='添加定时任务', type='info', icon='el-icon-document')
    def add_periodic_task(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        crontab = request.POST.get('crontab')
        enabled = request.POST.get('enabled')
        print(crontab, enabled)
        enabled = enabled == 'true'
        if not crontab:
            return JsonResponse(data={'status': 'error', 'msg': '请选输入执行计划'})
        try:
            minute, hour, day_of_month, month_of_year, day_of_week = crontab.split(' ')
        except Exception:
            return JsonResponse(data={'status': 'error', 'msg': 'crontab格式不正确'})

        for testplan in queryset:
            if testplan.periodic_task:
                print('更新定时任务')
                testplan.periodic_task.crontab = CrontabSchedule.objects.create(minute=minute, hour=hour,
                                                                                day_of_month=day_of_month,
                                                                                month_of_year=month_of_year,
                                                                                day_of_week=day_of_week)
                testplan.periodic_task.save()
            else:
                crontab = CrontabSchedule.objects.create(minute=minute, hour=hour, day_of_month=day_of_month,
                                                         month_of_year=month_of_year, day_of_week=day_of_week)
                testplan.periodic_task = PeriodicTask.objects.create(
                    name='%s-定时任务' % testplan.name,
                    crontab=crontab,
                    kwargs={'testplan_id': testplan.id, 'env_id': 1, 'user_id': request.user.id},
                    enabled=enabled
                )
                testplan.save()


        return JsonResponse(data={'status': 'success', 'msg': f'创建定时任务成功'})

    add_periodic_task.layer = {
        'title': '添加定时任务',
        'width': '35%',
        'params': [
            {
                'type': 'input',
                'tips': '*(分钟) *(小时) *(日期) *(月) *(星期)',
                'width': '300px',
                'key': 'crontab',
                'label': '执行计划',
                'require': True,
            },
            {
                'type': 'switch',
                'key': 'enabled',
                'label': '启用',
            },
        ]
    }
