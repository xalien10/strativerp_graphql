# Generated by Django 2.1.2 on 2019-03-27 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20181224_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='monthly_committed_hour',
            field=models.IntegerField(default=0, verbose_name='monthly committed hour'),
        ),
    ]
