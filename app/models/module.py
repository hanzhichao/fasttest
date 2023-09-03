from django.db import models
from app.models import BaseModel, NULLABLE_FK


class Module(BaseModel):
    parent = models.ForeignKey('self', verbose_name='上级模块', related_name='sub_modules',
                               **NULLABLE_FK)
    order = models.PositiveIntegerField('排序', default=0)

    def __str__(self):
        if self.parent:
            return '%s/%s' % (self.parent.name, self.name)
        return self.name


    class Meta:
        ordering = ['name']
        verbose_name = '用例模块'
        verbose_name_plural = '用例模块'
