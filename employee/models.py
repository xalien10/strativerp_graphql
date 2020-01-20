import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import BaseModel
from employee.helper import number_of_days_in_date_range
from payroll.models import Salary
from project.models import ProjectEmployee
from reporting.models import ReportedHour


class EmployeeType(models.Model):
    company = models.ForeignKey(to='company.Company', verbose_name=_('company'), related_name='employee_types',
                                on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('name'), max_length=100)
    type_weight = models.PositiveSmallIntegerField(verbose_name=_('weight'), null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    NUMBER_OF_MONTHLY_WORKING_DAYS = 22
    ACTIVE, INACTIVE = 'active', 'inactive'
    STATUS_CHOICE = ((ACTIVE, _('Active')), (INACTIVE, _('Inactive')))

    email = models.EmailField(verbose_name=_('email'), max_length=100, unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'),
                             related_name='employees', null=True, blank=True)
    company = models.ForeignKey(to='company.Company', on_delete=models.CASCADE, verbose_name=_('company'),
                                related_name='employees')
    group = models.ForeignKey(to='auth.Group', verbose_name=_('group'), related_name='employees',
                              on_delete=models.CASCADE)
    designation = models.CharField(verbose_name=_('designation'), max_length=100, null=True, blank=True)

    contact = models.ForeignKey(to='contact.Contact', on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(to='contact.Address', on_delete=models.CASCADE, null=True, blank=True)
    resume = models.FileField(verbose_name=_('resume'), upload_to='resume/', null=True, blank=True)
    monthly_committed_hour = models.IntegerField(verbose_name=_('committed hour( monthly )'), default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default=ACTIVE, verbose_name='status')

    def __str__(self):
        return self.user.get_full_name() if self.user else self.email

    def get_username(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.email

    def salary(self):
        s = self.salaries.all()
        return s[0] if s.exists() else None

    def get_project(self):
        projects = ProjectEmployee.objects.filter(employee=self)
        return projects

    def get_employee_salary(self):
        salary = Salary.objects.get(employee=self)
        return salary.get_hourly_salary()

    def get_hourly_salary(self):
        return self.get_employee_salary()

    def get_this_month_cost(self):
        salary = self.get_employee_salary()
        cost = salary * Decimal(self.reported_hours())
        return cost

    def get_total_cost(self):
        salary = self.get_employee_salary()
        cost = salary * Decimal(self.total_reported_hours())
        return cost

    def total_project_income(self, date_from=None, date_to=None):
        income = 0
        for project in self.get_project():
            report_hours_queryset = ReportedHour.objects.filter(project_employee_id=project.id, is_billable=True)
            if date_from and date_to:
                report_hours_queryset = report_hours_queryset.filter(date__gt=date_from, date__lte=date_to)
            total_hours = 0
            for report in report_hours_queryset:
                total_hours += report.hours
                total_hours += (report.minute / 60)
            income += total_hours * project.project.income
        return income

    def project_income(self, days=30):
        date_from = datetime.datetime.today() - datetime.timedelta(days=days)
        date_to = datetime.datetime.now()
        income = 0
        for project in self.get_project():
            report_hours_queryset = ReportedHour.objects.filter(project_employee_id=project.id,
                                                                date__lte=date_to, date__gt=date_from)

            total_hours = 0
            for report in report_hours_queryset:
                total_hours += report.hours
            income += total_hours * project.project.income
        return income

    def reported_hours(self, days=30, is_billable=None):
        date_from = datetime.datetime.today() - datetime.timedelta(days=days)
        date_to = datetime.datetime.now()
        return self.reported_hours_in_range(start_from=date_from, end_to=date_to, is_billable=is_billable)

    def total_reported_hours(self, start_from=None, end_to=None, is_billable=None):
        reports = ReportedHour.objects.filter(project_employee_id__employee=self)
        if start_from and end_to:
            reports = reports.filter(date__gte=start_from, date__lte=end_to)
        if is_billable != None:
            reports = reports.filter(is_billable=is_billable)

        total_reported_minutes = 0
        for report in reports:
            total_reported_minutes += report.hours * 60
            total_reported_minutes += report.minute
        total_reported_hours = total_reported_minutes / 60
        return total_reported_hours

    def total_billable_reported_hours(self, start_from=None, end_to=None):
        return self.total_reported_hours(start_from=start_from, end_to=end_to, is_billable=True)

    def contribution_profit(self):
        salary = Salary.objects.get(employee=self)
        income = self.total_project_income()
        cost = salary.get_hourly_salary() * Decimal(self.total_reported_hours())
        profit = income - cost
        return round(profit, 2)

    def occupancy(self):
        if self.monthly_committed_hour == 0:
            return 100.00
        else:
            occupancy = (self.reported_hours() / self.monthly_committed_hour) * 100
            return round(occupancy, 2)

    def reported_hours_in_range(self, start_from, end_to, is_billable=None):
        reports_in_duration = ReportedHour.objects.filter(project_employee_id__employee=self,
                                                          date__gte=start_from,
                                                          date__lte=end_to)
        if is_billable != None:
            reports_in_duration = reports_in_duration.filter(is_billable=is_billable)

        total_reported_minutes = 0
        for report in reports_in_duration:
            total_reported_minutes += report.hours * 60
            total_reported_minutes += report.minute
        total_reported_hours = float(total_reported_minutes) / 60
        return total_reported_hours

    def committed_hour_in_range(self, start_from, end_to):
        number_of_days = number_of_days_in_date_range(start_from, end_to)
        return float(self.monthly_committed_hour * number_of_days) / self.NUMBER_OF_MONTHLY_WORKING_DAYS

    def occupancy_in_range(self, start_from, end_to, is_billable=None):
        occupancy = 0.00
        committed_hour = self.committed_hour_in_range(start_from, end_to)
        if is_billable != None:
            reported_hour = self.reported_hours_in_range(start_from, end_to, is_billable=is_billable)
        else:
            reported_hour = self.reported_hours_in_range(start_from, end_to)

        if committed_hour == 0 and is_billable == True:
            occupancy = 0.00
        elif committed_hour == 0 and is_billable != True:
            occupancy = 100.00
        else:
            occupancy = round((float(reported_hour) / committed_hour) * 100, 2)

        return occupancy
