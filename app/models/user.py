from django.contrib.auth.models import User
from django.db import models


def __user__str__(self):
    if self.last_name and self.first_name:
        return '%s%s' % (self.last_name, self.first_name)
    return self.username


User.__str__ = __user__str__


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='系统用户', related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField('头像', null=True, blank=True, upload_to='avatars/')
    mobile = models.CharField('手机号码', max_length=11, null=True, blank=True)
    role = models.CharField('角色', max_length=20, null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=(('male', '男'), ('female', '女')), default='male')
    birthday = models.DateField('生日', null=True, blank=True)
    address = models.CharField('地址', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.user.username
