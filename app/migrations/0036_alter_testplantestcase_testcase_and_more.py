# Generated by Django 4.0 on 2023-09-05 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_alter_testplan_retry_interval_alter_testplan_timeout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplantestcase',
            name='testcase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_testplans', to='app.testcase', verbose_name='测试用例'),
        ),
        migrations.AlterUniqueTogether(
            name='testplantestcase',
            unique_together={('testcase', 'testplan')},
        ),
    ]
