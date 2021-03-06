# Generated by Django 2.1.2 on 2018-11-01 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0002_auto_20181101_1341'),
        ('reporting', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reportedhour',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportedhour_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='reportedhour',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_hours', to='project.ProjectEmployee', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='reportedhour',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportedhour_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
    ]
