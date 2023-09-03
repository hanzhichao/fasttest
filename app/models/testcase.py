import sys
from io import StringIO

from django.db import models
from taggit.managers import TaggableManager

from . import (BaseModelWithUser, Module, NULLABLE_FK, PRIORITY_CHOICES, TESTCASE_STATUS_CHOICES)


class capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


class TestCase(BaseModelWithUser):
    module = models.ForeignKey(Module, verbose_name='用例模块', **NULLABLE_FK)
    priority = models.PositiveSmallIntegerField('优先级',
                                                choices=PRIORITY_CHOICES, default=1)
    tags = TaggableManager('标签', blank=True)

    last_status = models.PositiveSmallIntegerField('运行状态', null=True, choices=TESTCASE_STATUS_CHOICES, default=0)
    last_result = models.TextField('运行日志', null=True, blank=True)

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'

    @property
    def setup_steps(self):
        return self.all_steps.filter(type=1)

    @property
    def test_steps(self):
        return self.all_steps.filter(type=0)

    @property
    def teardown_steps(self):
        return self.all_steps.filter(type=2)

    def run_setup_steps(self, env):
        for step in self.setup_steps:
            step.run(env)

    def run_teardown_steps(self, env):
        for step in self.teardown_steps:
            step.run(env)

    def run_test_steps(self, env):
        for step in self.test_steps:
            step.run(env)

    def run(self, env):
        # 输出流重定向
        print(f'运行用例 {self.name}')
        with capturing() as output:
            self.run_setup_steps(env)
            self.run_test_steps(env)
            self.run_teardown_steps(env)

        print('运行结果')
        result = '\n'.join(output)
        print(result)
        self.last_result = result
        self.save()
