# Generated by Django 2.1.2 on 2018-12-13 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0005_auto_20181209_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('salary_freq', models.CharField(choices=[('daily', 'daily'), ('hourly', 'Hourly'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='monthly', max_length=50, verbose_name='salary frequency')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='description')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salaries', to='employee.Employee', verbose_name='employee')),
            ],
        ),
    ]