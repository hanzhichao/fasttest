# Generated by Django 4.0 on 2023-09-04 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_module_options_alter_testrecord_testreport'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testrecord',
            options={'verbose_name': '测试纪录', 'verbose_name_plural': '测试纪录'},
        ),
    ]