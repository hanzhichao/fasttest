from django.db import models

from app.models.base import BaseModel


class Resource(BaseModel):
    data = models.JSONField('数据', null=True, blank=True, default=dict, )
    data_file = models.FileField('数据文件', null=True, blank=True, upload_to='resources')

    class Meta:
        verbose_name = '测试资源'
        verbose_name_plural = '测试资源'
