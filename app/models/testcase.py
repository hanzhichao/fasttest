from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from django.db import models
from taggit.managers import TaggableManager

from .base import BaseModel, BaseModelWithUser, NULLABLE_FK, PRIORITY_CHOICES


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


class TestCase(BaseModelWithUser):
    category = models.ForeignKey(Category, verbose_name='用例分类', **NULLABLE_FK)
    priority = models.PositiveSmallIntegerField('优先级',
                                                choices=PRIORITY_CHOICES, default=1)
    tags = TaggableManager('标签', blank=True)


    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'

    @property
    def last_result(self):
        return self.records.last()

    @property
    def last_status(self):
        last_result = self.last_result
        if last_result:
            return last_result.status

    @property
    def setup_steps(self):
        return self.all_steps.filter(type=1)

    @property
    def test_steps(self):
        return self.all_steps.filter(type=0)

    @property
    def teardown_steps(self):
        return self.all_steps.filter(type=2)


