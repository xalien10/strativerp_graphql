# Generated by Django 2.1.2 on 2018-12-09 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20181101_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedhour',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportedhour_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
    ]
