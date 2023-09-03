from django.contrib.auth.models import User
from django.db import models


TESTCASE_STATUS_CHOICES = (
    (0, '待运行'),
    (1, '通过'),
    (2, '失败'),
    (3, '异常'),
)
TESTPLAN_STATUS_CHOICES = (
    (0, '待运行'),
    (1, '全部通过'),
    (2, '部分失败'),
)

PRIORITY_CHOICES = (
    (0, 'P0'),
    (1, 'P1'),
    (2, 'P2'),
)

STEP_TYPE_CHOICES = (
    (0, '测试步骤'),
    (1, '测试准备'),
    (2, '测试清理'),
)

NULLABLE_FK = dict(null=True, blank=True, on_delete=models.SET_NULL)


class BaseModel(models.Model):
    name = models.CharField('名称', max_length=128)
    description = models.CharField('描述', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BaseModelWithUser(BaseModel):
    create_user = models.ForeignKey(User, verbose_name='创建人', related_name='created_%(class)s', **NULLABLE_FK)
    update_user = models.ForeignKey(User, verbose_name='修改人',related_name='updated_%(class)s', **NULLABLE_FK)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
