# Generated by Django 2.1.2 on 2018-11-01 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('project_type', models.CharField(choices=[('internal', 'Internal'), ('external', 'External')], default='external', max_length=30, verbose_name='project type')),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='budget')),
                ('income_type', models.CharField(blank=True, choices=[('fixed_cost', 'Fixed'), ('daily_cost', 'Daily'), ('hourly_cost', 'Hourly'), ('weekly_cost', 'Weekly')], max_length=30, null=True, verbose_name='income type')),
                ('income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='income')),
                ('estimation_type', models.CharField(blank=True, choices=[('daily', 'daily'), ('hourly', 'Hourly'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=30, null=True, verbose_name='estimation type')),
                ('estimated_time', models.PositiveIntegerField(default=0, verbose_name='estimated time')),
                ('starting_date', models.DateField(verbose_name='starting date')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='delivery date')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')], default='active', max_length=30, verbose_name='status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='company.Company', verbose_name='company')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_as', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_employees', to='employee.EmployeeType', verbose_name='assigned as')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_employees', to='employee.Employee', verbose_name='employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_employees', to='project.Project', verbose_name='project')),
            ],
        ),
    ]
