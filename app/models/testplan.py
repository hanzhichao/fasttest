from django.db import models

from django.db import models

from .base import BaseModelWithUser
from .testcase import TestCase


class TestPlan(BaseModelWithUser):
    """测试计划"""
    testcases = models.ManyToManyField(TestCase, verbose_name='测试用例', blank=True)

    # last_status = models.PositiveSmallIntegerField('运行状态', null=True, choices=TESTPLAN_STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = '测试计划'
        verbose_name_plural = '测试计划'

    @property
    def last_result(self):
        return self.reports.last()

    @property
    def last_status(self):
        last_result = self.last_result
        if last_result:
            return last_result.status

    def run(self, env):
        print('运行测试计划')
        for testcase in self.testcases.all():
            testcase.run(env)
