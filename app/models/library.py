from adminsortable.models import SortableMixin
from django.db import models

from .base import BaseModel
from ..utils import load_libs


class Library(BaseModel):
    init_args_schema = models.JSONField("初始化参数格式", blank=True, null=True, default=dict)
    enabled = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '操作库'
        verbose_name_plural = '操作库'

    def get_lib(self, config: dict = None):
        libs = load_libs(config)
        print('libs', libs)
        return libs.get(self.name)


class Method(BaseModel, SortableMixin):
    library = models.ForeignKey(Library, verbose_name='所属操作库', related_name='methods', on_delete=models.CASCADE)
    args_schema = models.JSONField("参数格式", blank=True, null=True, default=dict)
    order = models.PositiveIntegerField('排序', default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = '操作方法'
        verbose_name_plural = '操作方法'

    def get_method(self, config):
        lib = self.library.get_lib(config)
        method = getattr(lib, self.name)
        return method
