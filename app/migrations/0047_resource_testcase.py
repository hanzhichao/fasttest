# Generated by Django 4.0 on 2023-09-14 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='testcase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources', to='app.testcase', verbose_name='所属用例'),
        ),
    ]
