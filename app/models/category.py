from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models

from app.models.base import BaseModel, NULLABLE_FK, label


class Category(BaseModel, SortableMixin):
    parent = SortableForeignKey('self', verbose_name='上级分类', related_name='children',**NULLABLE_FK)
    order = models.PositiveIntegerField('排序', default=0)

    def __str__(self):
        if self.parent:
            return '%s/%s' % (self.parent.name, self.name)
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = '用例分类'
        verbose_name_plural = '用例分类'

    @property
    @label('级别')
    def level(self):
        if self.parent:
            return self.parent.level + 1
        return 0

    @property
    def all_testcases(self):
        qs = self.testcases.all()
        if self.children:
            for child in self.children.all():
                qs = qs.union(child.testcases.all())
        return qs
