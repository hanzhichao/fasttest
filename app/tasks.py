import logging
import os
import traceback
from pprint import pprint

from celery import shared_task
from django.utils.timezone import now

from app.models.env import Env
from app.models.step import Step
from app.models.testcase import TestCase
from app.models.testplan import TestPlan
from app.models.testreport import TestRecord, TestReport
from app.utils import Capturing, Context, gen_pass_rate_chart
from fasttest import settings

from loguru import logger

logger.add("django.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="100 MB", filter="",
           level="INFO", encoding='utf-8')



def run_step(step_id, context):
    step = Step.objects.get(id=step_id)
    print(f'执行步骤 {step} ----------------------------------------------------------------')
    # print('当前上下文变量', context.variables)
    method = step.method
    library = method.library

    method = context.get_method(library.name, method.name)
    print(f'执行操作: {step.method} 参数 {step.args} ')
    method_args = step.args

    if method_args is None:
        args, kwargs = [], {}
    elif isinstance(method_args, dict):
        args, kwargs = [], method_args
    elif isinstance(method_args, list):
        args, kwargs = method_args, {}
    else:
        args, kwargs = [method_args], {}

    args = [context.get(item) for item in args]
    kwargs = {key: context.get(value) for key, value in kwargs.items()}
    result = method(*args, **kwargs)
    context.set('result', result)
    if result:
        print(f'执行结果:')
        if isinstance(result, dict) or isinstance(result, list):
            pprint(result)
    return result


@shared_task
def run_testcase(testcase_id, env_id):
    testcase = TestCase.objects.get(id=testcase_id)
    env = Env.objects.get(id=env_id)
    context = Context(config = env.config, variables=env.variables)

    test_record = TestRecord(testcase=testcase, start_time=now())
    with Capturing() as output:
        print(f'运行用例 {testcase.name}')
        try:
            print('执行Setups >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            for step in testcase.setup_steps:
                run_step(step.id, context)
        except Exception:
            test_record.error_msg = traceback.format_exc()
            test_record.status = 2
        else:
            try:
                print('执行测试步骤 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                for step in testcase.test_steps:
                    run_step(step.id, context)
            except AssertionError:
                test_record.error_msg = traceback.format_exc()
                test_record.status = 2
            except Exception:
                test_record.error_msg = traceback.format_exc()
                test_record.status = 3
            else:
                test_record.status = 1
            finally:
                try:
                    print('执行Teardowns >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                    for step in testcase.teardown_steps:
                        run_step(step.id, context)
                except:
                    pass
    test_record.end_time = now()
    log = '\n'.join(output)
    print('运行结果')
    print(log)
    test_record.log = log
    test_record.save()
    return test_record.id


@shared_task
def run_testplan(testplan_id, env_id):
    testplan = TestPlan.objects.get(id=testplan_id)
    test_report = TestReport(testplan=testplan, start_time=now(), status=1)
    test_report.save()
    for testcase in testplan.testcases.all():
        test_record_id = run_testcase(testcase.id, env_id)
        test_record = TestRecord.objects.get(id=test_record_id)
        test_record.testreport = test_report
        test_record.save()
        if test_record.status == 1:
            test_report.pass_num += 1
        elif test_record.status == 2:
            test_report.fail_num += 1
        elif test_record.status == 3:
            test_report.error_num += 1
        test_report.total += 1
    test_report.end_time = now()

    output_dir = settings.MEDIA_ROOT / 'reports' / f'{test_report.id}'
    if not output_dir.exists():
        os.makedirs(output_dir)
    image_file = str(output_dir / 'pass_rate.png')
    gen_pass_rate_chart(test_report.pass_num, test_report.fail_num, test_report.error_num, image_file)

    test_report.chart = f'reports/{test_report.id}/pass_rate.png'
    test_report.save()
