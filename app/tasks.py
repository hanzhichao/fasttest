from celery import shared_task
from django.utils.timezone import now

from app.models.env import Env
from app.models.testcase import TestCase
from app.models.testplan import TestPlan
from app.models.testreport import TestReport
from app.runner import run_testcase


@shared_task(name='运行测试用例')
def run_testcase_task(testcase_id: int, env_id: int, user_id: int, test_report_id: int = None) -> int:
    testcase = TestCase.objects.get(id=testcase_id)
    env = Env.objects.get(id=env_id)
    return run_testcase(testcase, env, user_id, test_report_id).id


@shared_task(name='运行测试计划')
def run_testplan_task(testplan_id: int, env_id: int, user_id: int) -> int:
    testplan = TestPlan.objects.get(id=testplan_id)
    # env = Env.objects.get(id=env_id)
    test_report = TestReport.objects.create(testplan=testplan, env_id=env_id,
                                            create_user_id=user_id,
                                            start_time=now())
    for testcase in testplan.testcases.all():
        run_testcase_task.delay(testcase.id, env_id, user_id, test_report.id)

    return test_report.id
