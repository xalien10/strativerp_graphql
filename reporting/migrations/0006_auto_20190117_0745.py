# Generated by Django 2.1.2 on 2019-01-17 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0005_auto_20181224_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportedhour',
            old_name='project',
            new_name='project_employee',
        ),
    ]
