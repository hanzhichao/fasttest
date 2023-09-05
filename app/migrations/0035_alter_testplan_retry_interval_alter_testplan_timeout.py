# Generated by Django 4.0 on 2023-09-05 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_testplan_retry_interval_testplan_retry_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='retry_interval',
            field=models.PositiveIntegerField(blank=True, default=1, help_text='单位s', null=True, verbose_name='失败重试间隔'),
        ),
        migrations.AlterField(
            model_name='testplan',
            name='timeout',
            field=models.PositiveIntegerField(blank=True, default=60, help_text='单位s', null=True, verbose_name='超时时间'),
        ),
    ]
