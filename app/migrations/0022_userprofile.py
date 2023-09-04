# Generated by Django 4.0 on 2023-09-04 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0021_remove_testplan_env'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='头像')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码')),
                ('role', models.CharField(blank=True, max_length=20, null=True, verbose_name='角色')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='地址')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user', verbose_name='系统用户')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]