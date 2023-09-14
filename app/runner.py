import importlib
import os
import re
import sys
import traceback
from collections import ChainMap
from functools import reduce
from io import StringIO
from pprint import pprint

from django.utils.timezone import now

from app.models.env import Env
from app.models.step import Step
from app.models.testcase import TestCase
from app.models.testplan import TestPlan
from app.models.testrecord import TestRecord
from app.models.testreport import TestReport
from fasttest import settings

DOLLAR_VARIABLE = re.compile('\${?([\w.]+)}?')
PURE_DOLLAR_VARIABLE = re.compile('^\${?([\w.]+)}?$')


# 输出流重定向（捕获屏幕标准输出和标准错误输出）


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout  # 备份一份原系统输出流
        sys.stdout = self._stringio1 = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio1.getvalue().splitlines())
        del self._stringio1  # free up some memory
        sys.stdout = self._stdout


class Context:
    def __init__(self, config: dict = None, variables=None):
        variables = variables or {}
        self.config = config or {}
        self.variables = ChainMap(variables, os.environ)
        self.libraries = self.get_libraries()

    def get_libraries(self):
        libraries = {}
        for lib_config in settings.TEST_LIBRARIES:
            # TEST_LIBRARIES = [
            #     {'Common': 'libs.commonlib'},
            #     {'Assert': 'libs.assertlib'},
            #     {'Http': 'libs.httplib'},
            #     {'Selenium': 'libs.seleniumlib'},
            # ]
            # lib_config = {'Http': 'libs.httplib'}

            for class_name, module_path in lib_config.items():
                # class_name= Http， module_path ='libs.httplib'
                module = importlib.import_module(module_path)

                # lib_class = class Http
                lib_class = getattr(module, class_name)
                # 获取类的初始化参数
                # self.config = {'Http': {'base_url': ''}}
                init_args = self.config.get(class_name, {})

                # lib = Http(base_url='')
                lib = lib_class(**init_args)

                libraries[class_name] = lib
        # {'Http':  Http(base_url=''), ...}
        return libraries

    def get_method(self, library_name, method_name):
        library = self.libraries.get(library_name, None)
        method = getattr(library, method_name)
        return method

    @staticmethod
    def do_dot(item, key: str):
        """单个content.url取值"""  # result.url
        if hasattr(item, key):
            return getattr(item, key)

        if key.isdigit():  # result.1  # []
            key = int(key)
        try:
            return item[key]  # result[1] / result[key]

        except Exception as ex:
            return key  # result.url

    def repl_func(self, matched):
        if matched:
            text = matched.group(1)
            return str(self.get_field(text))

    def get_field(self, expr: str):
        """解析形如content.result.0.id的取值"""
        if '.' in expr:
            value = expr.split('.')
            field = self.variables.get(value[0])
            return reduce(lambda x, y: self.do_dot(x, y), value[1:], field)
        else:
            return self.variables.get(expr)

    def get(self, expr: str):
        if not isinstance(expr, str):
            return expr
        if DOLLAR_VARIABLE.match(expr):
            matched = PURE_DOLLAR_VARIABLE.match(expr)
            if matched:
                return self.get_field(matched.group(1))
            return re.sub(DOLLAR_VARIABLE, self.repl_func, expr)
        return self.variables.get(expr, expr)

    def set(self, key, value):
        if not isinstance(key, str):
            key = str(key)
        if isinstance(value, str):
            value = self.get(value)
        self.variables.update({key: value})


def run_step(step: Step, context: Context):
    print(f' 执行步骤 {step} ----------------------------------------------------------------')
    # print('当前上下文变量', context.variables)
    method = step.method
    library = method.library

    method = context.get_method(library.name, method.name)
    print(f' 执行操作: {step.method} 参数 {step.args} ')
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
        print(f' 执行结果:')
        if isinstance(result, dict) or isinstance(result, list):
            pprint(result)
    return result


def run_testcase(testcase: TestCase, env, user_id: int, testreport_id: int = None) -> TestRecord:
    context = Context(config=env.config, variables=env.variables)
    test_record = TestRecord(testcase=testcase, env=env, create_user_id=user_id, start_time=now(),
                             testreport_id=testreport_id)
    for resource in testcase.resources.all():
        if resource.data_file is not None:
            context.set(resource.name, resource.data_file)
        else:
            context.set(resource.name, resource.data)

    print('context ********************************')
    print(context)

    with Capturing() as output:
        print(f'运行用例 {testcase.name}')
        try:
            print('>>> 执行Setups')
            for step in testcase.setup_steps:
                run_step(step, context)
        except Exception:
            test_record.error_msg = traceback.format_exc()
            test_record.status = 2
        else:
            try:
                print('>>> 执行测试步骤')
                for step in testcase.test_steps:
                    run_step(step, context)
            except AssertionError:
                test_record.error_msg = traceback.format_exc()
                print('<<< 用例失败\n')
                print(test_record.error_msg)
                test_record.status = 2
            except Exception:
                test_record.error_msg = traceback.format_exc()
                print('<<< 用例出错\n')
                print(test_record.error_msg)
                test_record.status = 3
            else:
                print('<<< 用例成功\n')
                test_record.status = 1
            finally:
                try:
                    print('>>> 执行Teardowns')
                    for step in testcase.teardown_steps:
                        run_step(step, context)
                except:
                    pass
    test_record.end_time = now()
    log = '\n'.join(output)
    print('运行结果')
    print(log)
    test_record.log = log
    test_record.save()
    return test_record


def run_testplan(testplan: TestPlan, env: Env, user_id: int) -> TestReport:
    test_report = TestReport.objects.create(testplan=testplan, env=env, create_user_id=user_id,
                                            start_time=now())
    for testcase in testplan.testcases.all():
        test_record = run_testcase(testcase, env, user_id, test_report)
        # test_record.testreport = test_report
        # test_record.save()
    #     if test_record.status == 1:
    #         test_report.pass_num += 1
    #     else:
    #         test_report.status = 2
    #         if test_record.status == 2:
    #             test_report.fail_num += 1
    #         elif test_record.status == 3:
    #             test_report.error_num += 1
    #
    #     test_report.total += 1
    # test_report.end_time = now()
    # test_report.save()
    return test_report
