# Generated by Django 4.0 on 2023-09-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_testcase_last_result'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['order'], 'verbose_name': '步骤', 'verbose_name_plural': '步骤'},
        ),
        migrations.AlterModelOptions(
            name='testcase',
            options={'ordering': ['order'], 'verbose_name': '测试用例', 'verbose_name_plural': '测试用例'},
        ),
        migrations.AddField(
            model_name='step',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='排序'),
        ),
    ]
