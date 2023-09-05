# Generated by Django 4.0 on 2023-09-05 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_testcase_options_remove_testcase_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testplan',
            name='testcases',
        ),
        migrations.CreateModel(
            name='TestPlanTestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='排序')),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_testplans', to='app.testcase', verbose_name='测试用例')),
                ('testplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_testcases', to='app.testplan', verbose_name='测试计划')),
            ],
            options={
                'verbose_name': '测试用例关联',
                'verbose_name_plural': '测试用例关联',
                'ordering': ['order'],
            },
        ),
    ]