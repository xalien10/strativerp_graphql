# Generated by Django 2.1.2 on 2019-09-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20190403_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=30, verbose_name='status'),
        ),
    ]
