# Generated by Django 2.1.2 on 2018-12-07 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20181112_0915'),
        ('employee', '0003_auto_20181113_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contact.Address'),
        ),
        migrations.AddField(
            model_name='employee',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='resume'),
        ),
    ]
