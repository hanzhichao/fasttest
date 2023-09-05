# Generated by Django 4.0 on 2023-09-05 03:42

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_testplan_testcases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testcases', to='app.category', verbose_name='用例分类'),
        ),
        migrations.AlterField(
            model_name='testplantestcase',
            name='testplan',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_testcases', to='app.testplan', verbose_name='测试计划'),
        ),
    ]