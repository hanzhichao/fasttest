from django.db import models

from app.models import BaseModel


class Env(BaseModel):
    config = models.JSONField('测试库配置', null=True, default=dict)

    class Meta:
        verbose_name = '测试环境'
        verbose_name_plural = '测试环境'


class EnvVariable(models.Model):
    env = models.ForeignKey(Env, verbose_name='所属环境', on_delete=models.CASCADE)
    key = models.CharField('变量名', max_length=128)
    value = models.JSONField('变量值', null=True, default=dict)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = '环境变量'
        verbose_name_plural = '环境变量'
