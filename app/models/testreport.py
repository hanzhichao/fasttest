from django.db import models

from . import (TESTCASE_STATUS_CHOICES, TESTPLAN_STATUS_CHOICES)


class TestReport(models.Model):
    testplan = models.ForeignKey("TestPlan", verbose_name='测试计划', related_name='reports', on_delete=models.CASCADE)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.PositiveSmallIntegerField('运行状态', null=True, choices=TESTPLAN_STATUS_CHOICES, default=0)

    total = models.PositiveIntegerField('运行总数', default=0)
    fail_num = models.PositiveIntegerField('失败用例数', default=0)
    pass_num = models.PositiveIntegerField('通过用例数', default=0)

    @property
    def is_success(self):
        if self.status is not None:
            return self.status == 1

    @property
    def pass_rate(self):
        if self.total > 0:
            pass_rate = round(self.pass_num * 100/ self.total, 2)
            return f'{pass_rate}%'

    def __str__(self):
        return '%s-测试报告-%s' % (self.testplan.name, self.start_time)

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告'


class TestRecord(models.Model):
    """测试报告中-单条用例的执行纪录"""
    testreport = models.ForeignKey("TestReport", verbose_name='测试报告', related_name='details',
                                   on_delete=models.CASCADE)
    testcase = models.ForeignKey("TestCase", verbose_name='测试报告', related_name='records', on_delete=models.CASCADE)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.PositiveSmallIntegerField('运行状态', null=True,
                                              choices=TESTCASE_STATUS_CHOICES, default=0)
    error_msg = models.TextField('错误信息', null=True)
    details = models.JSONField('步骤详情', null=True, default=dict)

    def __str__(self):
        return '%s-测试纪录-%s' % (self.testcase.name, self.start_time)

    class Meta:
        verbose_name = '测试纪录'
        verbose_name_plural = '测试报告'
