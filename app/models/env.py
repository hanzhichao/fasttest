import importlib
from functools import cached_property

from django.db import models

from fasttest import settings
from .base import BaseModel
from .library import Library


class Env(BaseModel):
    # config = models.JSONField('测试库配置', null=True, default=dict)

    class Meta:
        verbose_name = '测试环境'
        verbose_name_plural = '测试环境'

    @property
    def config(self):
        return {item.library.name: item.config for item in self.library_configs.all()}

    @property
    def variables(self):
        return {item.key: item.value for item in self.env_variables.all()}




class LibraryConfig(models.Model):
    env = models.ForeignKey(Env, verbose_name='所属环境', related_name='library_configs', on_delete=models.CASCADE)
    library = models.ForeignKey(Library, verbose_name='操作库', on_delete=models.CASCADE)
    config = models.JSONField('测试库配置', null=True, blank=True, default=dict, help_text='操作库类初始化参数,字典格式')

    def __str__(self):
        return '%s-操作库配置' % self.library.name

    class Meta:
        unique_together = ["env", "library"]
        verbose_name = '操作库配置'
        verbose_name_plural = '操作库配置'


class EnvVariable(models.Model):
    env = models.ForeignKey(Env, verbose_name='所属环境', related_name='env_variables', on_delete=models.CASCADE)
    key = models.CharField('变量名', max_length=128)
    value = models.JSONField('变量值', null=True, default=dict)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = '环境变量'
        verbose_name_plural = '环境变量'
