# Generated by Django 4.0 on 2023-09-06 11:28

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_remove_testreport_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='args',
            new_name='init_args_schema',
        ),
        migrations.RenameField(
            model_name='method',
            old_name='args',
            new_name='args_schema',
        ),
        migrations.AlterField(
            model_name='testplantestcase',
            name='testcase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testplan_testcases', to='app.testcase', verbose_name='测试用例'),
        ),
        migrations.AlterField(
            model_name='testplantestcase',
            name='testplan',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testplan_testcases', to='app.testplan', verbose_name='测试计划'),
        ),
        migrations.AlterUniqueTogether(
            name='envvariable',
            unique_together={('env', 'key')},
        ),
    ]