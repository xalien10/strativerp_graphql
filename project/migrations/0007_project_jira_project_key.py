# Generated by Django 2.1.2 on 2019-09-05 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20190905_0552'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='jira_project_key',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='jira project key'),
        ),
    ]
