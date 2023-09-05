from copy import copy

from django.db import models
from taggit.managers import TaggableManager

from .base import BaseModelWithUser, NULLABLE_FK, PRIORITY_CHOICES
from .category import Category


class TestCase(BaseModelWithUser):
    category = models.ForeignKey(Category, verbose_name='用例分类', related_name='testcases', **NULLABLE_FK)
    priority = models.PositiveSmallIntegerField('优先级',
                                                choices=PRIORITY_CHOICES, default=1)
    tags = TaggableManager('标签', blank=True)

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'

    def copy(self, name=None):
        name = name or '%s-复制' % self.name
        new_obj = copy(self)
        new_obj.pk, new_obj.name = None, name
        new_obj.save()

        for tag in self.tags.all():
            new_obj.tags.add(tag)

        for step in self.all_steps.all():
            step.pk, step.testcase = None, new_obj
            step.save()

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


