# Generated by Django 4.0 on 2023-09-06 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('django_celery_beat', '0018_improve_crontab_helptext'),
        ('app', '0037_alter_method_options_method_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='testplan',
            name='periodic_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask'),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to='auth.user', verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='env',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='app.env', verbose_name='运行环境'),
        ),
        migrations.AddField(
            model_name='testreport',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(class)s', to='auth.user', verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='testreport',
            name='env',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='app.env', verbose_name='运行环境'),
        ),
    ]
