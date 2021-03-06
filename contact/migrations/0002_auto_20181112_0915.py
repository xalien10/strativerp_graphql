# Generated by Django 2.1.2 on 2018-11-12 09:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Enter your valid contact number.', regex='(^[+0-9]{1,3})*([0-9]{10,11}$)')], verbose_name='mobile'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Enter your valid contact number.', regex='(^[+0-9]{1,3})*([0-9]{10,11}$)')], verbose_name='telephone'),
        ),
    ]
