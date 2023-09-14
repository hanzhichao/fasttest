from functools import cached_property

from django.db import models

from .base import (ERROR_REASON_CHOICES, NULLABLE_FK, TESTCASE_STATUS_CHOICES, User, label)
from .env import Env


class TestRecord(models.Model):
    """测试报告中-单条用例的执行纪录"""
    testreport = models.ForeignKey("TestReport", verbose_name='测试报告', related_name='details',
                                   **NULLABLE_FK)
    testcase = models.ForeignKey("TestCase", verbose_name='测试用例', related_name='records', on_delete=models.CASCADE)
    env = models.ForeignKey(Env, verbose_name='运行环境', related_name='records', **NULLABLE_FK)
    create_user = models.ForeignKey(User, verbose_name='执行人', related_name='created_%(class)s', **NULLABLE_FK)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.PositiveSmallIntegerField('运行状态', null=True,
                                              choices=TESTCASE_STATUS_CHOICES, default=0)
    error_msg = models.TextField('错误信息', null=True, blank=True, default='')
    error_reason = models.CharField('错误原因', max_length=128, null=True, blank=True, choices=ERROR_REASON_CHOICES)
    log = models.TextField('运行日志', null=True, blank=True, default='')

    def __str__(self):
        return '%s-测试纪录-%s' % (self.testcase.name, self.start_time.strftime('%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = '测试纪录'
        verbose_name_plural = '测试纪录'

    @cached_property
    @label('耗时')
    def elapsed_time(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
