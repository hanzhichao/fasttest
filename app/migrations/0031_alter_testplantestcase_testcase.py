# Generated by Django 4.0 on 2023-09-05 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_remove_testplan_testcases_testplantestcase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplantestcase',
            name='testcase',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_testplans', to='app.testcase', verbose_name='测试用例'),
        ),
    ]
