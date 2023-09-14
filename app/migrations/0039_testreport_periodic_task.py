# Generated by Django 4.0 on 2023-09-06 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
        ('app', '0038_testplan_periodic_task_testrecord_create_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testreport',
            name='periodic_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask'),
        ),
    ]
