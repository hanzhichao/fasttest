import os
from functools import cached_property

from django.db import models
from django_celery_beat.models import PeriodicTask

from fasttest import settings
from .base import (NULLABLE_FK, User, label)
from .env import Env
from .testplan import TestPlan
from ..utils import gen_pass_rate_chart


class TestReport(models.Model):
    testplan = models.ForeignKey(TestPlan, verbose_name='测试计划', related_name='reports', on_delete=models.CASCADE)
    periodic_task = models.ForeignKey(PeriodicTask, verbose_name='定时任务', **NULLABLE_FK)
    create_user = models.ForeignKey(User, verbose_name='执行人', related_name='created_%(class)s', **NULLABLE_FK)
    env = models.ForeignKey(Env, verbose_name='运行环境', related_name='reports', **NULLABLE_FK)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    chart = models.ImageField('运行统计', null=True, blank=True)
    # total = models.PositiveIntegerField('运行总数', null=True, blank=True, default=0)
    # pass_num = models.PositiveIntegerField('成功数', null=True, blank=True, default=0)
    # fail_num = models.PositiveIntegerField('失败数', null=True, blank=True, default=0)
    # error_num = models.PositiveIntegerField('错误数', null=True, blank=True, default=0)
    # status = models.PositiveIntegerField('运行状态', null=True, blank=True, choices=TESTPLAN_STATUS_CHOICES)
    # pass_rate = models.FloatField('通过率', null=True, blank=True, default=0)

    def __str__(self):
        return '%s-测试报告-%s' % (self.testplan.name, self.start_time.strftime('%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告'

    def statistics(self):
        if self.details:
            self.end_time = self.details.last().end_time
            self.total = self.details.count()
            self.fail_num = self.details.filter(status=2).count()
            self.pass_num = self.details.filter(status=1).count()
            self.error_num = self.details.filter(status=3).count()
            self.status = 1 if self.pass_num == self.total else 2
            self.pass_rate = round(self.pass_num * 100 / self.total, 2)
            self.save()

    @cached_property
    @label('总数')
    def total(self):
        return self.details.count() if self.details else 0

    @cached_property
    @label('结束时间')
    def end_time(self):
        if self.details.last():
            return self.details.last().end_time

    @cached_property
    @label('运行状态')
    def status(self):
        if self.total:
            return 1 if self.pass_num == self.total else 2
        return 0

    @cached_property
    @label('失败数')
    def fail_num(self):
        return self.details.filter(status=2).count() if self.details else 0

    @cached_property
    @label('成功数')
    def pass_num(self):
        return self.details.filter(status=1).count() if self.details else 0

    @cached_property
    @label('出错数')
    def error_num(self):
        return self.details.filter(status=3).count() if self.details else 0

    @cached_property
    @label('是否成功')
    def is_success(self):
        if self.status is not None:
            return self.status == 1

    @cached_property
    @label('耗时')
    def elapsed_time(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time

    @cached_property
    @label('通过率')
    def pass_rate(self):
        if self.total > 0:
            pass_rate = round(self.pass_num * 100 / self.total, 2)
            return f'{pass_rate}%'

    def get_chart(self):
        if not self.chart:
            output_dir = settings.MEDIA_ROOT / 'reports' / f'{self.id}'
            if not output_dir.exists():
                os.makedirs(output_dir)
            image_file = str(output_dir / 'pass_rate.png')
            gen_pass_rate_chart(self.pass_num, self.fail_num, self.error_num, image_file)
            self.chart = f'reports/{self.id}/pass_rate.png'
            self.save()
        return self.chart
