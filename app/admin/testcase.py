from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html

from app.admin.base import BaseModelAdmin, BaseTabularInline
from app.models import Env, SetupStep, TeardownStep, TestCase, TestStep


class TestStepInline(BaseTabularInline):
    model = TestStep
    exclude = ['type']


class SetupStepInline(BaseTabularInline):
    model = SetupStep
    exclude = ['type']


class TeardownStepInline(BaseTabularInline):
    model = TeardownStep
    exclude = ['type']


@admin.register(TestCase)
class TestCaseAdmin(BaseModelAdmin):
    # 列表页配置
    list_display = ['id', 'name', 'module', 'priority', 'tag_list', 'create_user', 'create_time', 'operation']
    list_display_links = ['name']
    actions = ['run']
    change_list_template = 'admin/testcase_list.html'
    # readonly_fields = ['last_status', 'last_result']

    # 修改页配置

    exclude = ['create_user', 'update_user', 'last_status', 'last_result']
    inlines = [SetupStepInline, TestStepInline, TeardownStepInline]

    @admin.display(description='标签')
    def tag_list(self, obj):
        return format_html(' '.join([
            f'<span class="el-tag el-tag--small el-tag--light">{tag.name}</span>'
            for tag in obj.tags.all()]))

    @admin.display(description='操作')
    def operation(self, obj):
        # last_result = format_html(obj.last_result)
        view_html = '''
        <div id="operation">
        <el-button type="text" @click="dialogFormVisible = true">查看</el-button>
        <el-dialog title="运行日志" :visible.sync="dialogFormVisible">
          <pre>%s</pre>
          <div slot="footer" class="dialog-footer">
          </div>
        <div>
        ''' % 'ok'
        return format_html(view_html)

    def operation_run(self, result, testcase_id):
        testcase = TestCase.objects.get(id=testcase_id)
        pass

    def operation_view_log(self, result, testcase_id):
        pass

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
        env = Env.objects.get(id=env_id)

        for obj in queryset:
            obj.run(env)

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
