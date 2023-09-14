from copy import copy

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from django_celery_beat.models import PeriodicTask

from .base import BaseModelWithUser, NULLABLE_FK, label
from .testcase import TestCase


class TestPlan(BaseModelWithUser):
    testcases = models.ManyToManyField(TestCase, verbose_name='测试用例', blank=True, through="TestPlanTestCase")

    timeout = models.PositiveIntegerField('超时时间', null=True, blank=True, default=60, help_text='单位s')
    retry_limit = models.PositiveIntegerField('失败重试次数', null=True, blank=True, default=0)
    retry_interval = models.PositiveIntegerField('失败重试间隔', null=True, blank=True, default=1, help_text='单位s')
    periodic_task = models.ForeignKey(PeriodicTask, verbose_name='定时任务', **NULLABLE_FK)

    class Meta:
        verbose_name = '测试计划'
        verbose_name_plural = '测试计划'

    @property
    def crontab(self):
        if self.periodic_task and self.periodic_task.crontab:
            return self.periodic_task.crontab

    @property
    def last_result(self):
        return self.reports.last()

    @property
    @label('上次运行状态')
    def last_status(self):
        last_result = self.last_result
        if last_result:
            return last_result.status

    @property
    @label('用例数')
    def testcase_cnt(self):
        return self.testcases.count()

    @property
    @label('运行次数')
    def results_cnt(self):
        return self.reports.count()




    def copy(self, name=None):
        name = name or '%s-复制' % self.name
        new_obj = copy(self)
        new_obj.pk, new_obj.name = None, name
        new_obj.save()

        for item in self.testplan_testcases.all():
            item.pk, item.testplan = None, new_obj
            item.save()


class TestPlanTestCase(SortableMixin):
    testplan = SortableForeignKey(TestPlan, verbose_name='测试计划', related_name='testplan_testcases',
                                  on_delete=models.CASCADE)
    testcase = models.ForeignKey(TestCase, verbose_name='测试用例', related_name='testplan_testcases',
                                 on_delete=models.CASCADE)

    order = models.PositiveIntegerField('排序', default=0, editable=False, db_index=True)
    timeout = models.PositiveIntegerField('超时时间', null=True, blank=True)

    def __str__(self):
        return self.testcase.name

    class Meta:
        unique_together = ["testcase", "testplan"]
        ordering = ['order']
        verbose_name = '测试用例关联'
        verbose_name_plural = '测试用例关联'
