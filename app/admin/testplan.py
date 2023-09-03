import traceback
from datetime import datetime

from django.contrib import admin
from django.http import JsonResponse

from app.admin.base import BaseModelAdmin
from app.models import Env, TestPlan, TestRecord, TestReport


@admin.register(TestPlan)
class TestPlanAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'description', 'testcase_cnt', 'last_status', 'create_user',
                    'create_time']
    list_display_links = ['name']
    exclude = ['create_user', 'update_user', 'last_status']

    filter_horizontal = ['testcases']

    actions = ['run']

    @admin.display(description='用例数')
    def testcase_cnt(self, obj):
        return obj.testcases.count()


    def run_testplan(self, testplan, env):
        test_report = TestReport(testplan=testplan, start_time = datetime.now(), status=1)
        test_report.save()
        for testcase in testplan.testcases.all():
            test_record = TestRecord(testreport=test_report, testcase=testcase,
                                     start_time=datetime.now())
            try:
                testcase.run(env)
            except AssertionError:
                test_record.error_msg = traceback.format_exc()
                test_record.status = 2
                test_report.status = 2
                test_report.fail_num +=1
            except Exception:
                test_record.error_msg = traceback.format_exc()
                test_record.status = 3
                test_report.status = 2
                test_report.fail_num += 1
            else:
                test_record.error_msg = traceback.format_exc()
                test_record.status = 1
                test_report.pass_num += 1
            test_record.end_time = datetime.now()
            test_record.save()
            test_report.total += 1

        test_report.end_time = datetime.now()
        test_report.save()



    @admin.action(description='运行')
    def run(self, request, queryset):
        if not request.POST.get('_selected'):
            return JsonResponse(data={'status': 'error', 'msg': '请先选中数据'})

        env_id = request.POST.get('env')
        if not env_id:
            return JsonResponse(data={'status': 'error', 'msg': '请选择环境'})
        env = Env.objects.get(id=env_id)

        for testplan in queryset:
            self.run_testplan(testplan, env)

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
