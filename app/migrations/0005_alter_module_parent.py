# Generated by Django 4.0 on 2023-09-03 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_module_tn_ancestors_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_modules', to='app.module', verbose_name='上级模块'),
        ),
    ]