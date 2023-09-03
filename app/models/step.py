from django.db import models

from . import (Method, NULLABLE_FK, STEP_TYPE_CHOICES, TestCase, BaseModel)
from ..managers import SetupStepManager, TeardownStepManager, TestStepManager


class Step(models.Model):
    testcase = models.ForeignKey(TestCase, verbose_name='所属用例',
                                 related_name='all_steps', on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField('步骤类型', choices=STEP_TYPE_CHOICES, default=0)
    name = models.CharField('名称', max_length=128, null=True, blank=True)
    method = models.ForeignKey(Method, verbose_name='操作方法', related_name='steps', **NULLABLE_FK)
    args = models.JSONField('方法参数', blank=True, null=True, default=dict)

    def __str__(self):
        return self.name or str(self.method) or ''

    def run(self, env):
        print(f'执行用例 env={env}')
        config = env.config
        method = self.method.get_method(config)
        print(f'执行操作: {self.method} 参数 {self.args} ')
        result = method(**self.args)
        print(f'执行结果: {result}')
        return result

    class Meta:
        verbose_name = '步骤'
        verbose_name_plural = '步骤'


class TestStep(Step):
    objects = TestStepManager()

    class Meta:
        proxy = True
        verbose_name = '测试步骤'
        verbose_name_plural = '测试步骤'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.type = 0
        super().save(force_insert, force_update, using, update_fields)


class SetupStep(Step):
    objects = SetupStepManager()

    class Meta:
        proxy = True
        verbose_name = '测试准备步骤'
        verbose_name_plural = '测试准备步骤'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.type = 1
        super().save(force_insert, force_update, using, update_fields)


class TeardownStep(Step):
    objects = TeardownStepManager()

    class Meta:
        proxy = True
        verbose_name = '测试清理步骤'
        verbose_name_plural = '测试清理步骤'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.type = 2
        super().save(force_insert, force_update, using, update_fields)
