from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.constants import COST_TYPE, TIME_ESTIMATION_TYPE
from base.models import BaseModel
from payroll.models import Salary
from project.constants import ACTIVE
from reporting.models import ReportedHour


class Project(BaseModel):
    ACTIVE, INACTIVE, PENDING = 'active', 'inactive', 'pending'
    STATUS_CHOICE = ((ACTIVE, _('Active')), (INACTIVE, _('Inactive')), (PENDING, _('Pending')))

    INTERNAL, EXTERNAL = 'internal', 'external'
    TYPE_CHOICE = ((INTERNAL, _('Internal')), (EXTERNAL, _('External')))

    company = models.ForeignKey(to='company.Company', related_name='projects', on_delete=models.CASCADE,
                                verbose_name=_('company'))
    name = models.CharField(max_length=100, verbose_name=_('name'))
    jira_project_key = models.CharField(max_length=50, verbose_name=_('jira project key'), unique=True, null=True)
    project_type = models.CharField(verbose_name=_('project type'), max_length=30, choices=TYPE_CHOICE,
                                    default=EXTERNAL)
    budget = models.DecimalField(verbose_name=_('budget'), max_digits=10, decimal_places=2, default=0)
    income_type = models.CharField(verbose_name=_('income type'), max_length=30, choices=COST_TYPE, null=True,
                                   blank=True)
    income_currency = models.ForeignKey(to='currency.Currency', verbose_name=_('currency'), related_name='projects',
                                        on_delete=models.CASCADE, null=True, blank=True)
    income = models.DecimalField(verbose_name=_('income'), max_digits=10, decimal_places=2, default=0)
    estimation_type = models.CharField(verbose_name=_('estimation type'), max_length=30, choices=TIME_ESTIMATION_TYPE,
                                       null=True, blank=True)
    estimated_time = models.PositiveIntegerField(verbose_name=_('estimated time'), default=0)
    starting_date = models.DateField(verbose_name=_('starting date'))
    delivery_date = models.DateField(verbose_name=_('delivery date'), null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default=ACTIVE, verbose_name='status')

    def __str__(self):
        return self.name

    @property
    def get_income_currency(self):
        return self.income_currency if self.income_currency else self.company.currency

    def get_hourly_income(self):
        income = 0
        if self.income_type == 'hourly_cost':
            income = self.income
        elif self.income_type == 'daily_cost':
            income = self.income / 5
        elif self.income_type == 'weekly_cost':
            income = self.income / 37.5

        return income

    def get_employee(self):
        employees = ProjectEmployee.objects.filter(project=self, status=ACTIVE)
        return employees

    class Meta:
        unique_together = ('company', 'name')


class ProjectEmployee(models.Model):
    ACTIVE, INACTIVE = 'active', 'inactive'
    STATUS_CHOICE = ((ACTIVE, _('Active')), (INACTIVE, _('Inactive')))

    project = models.ForeignKey(to='project.Project', verbose_name=_('project'), related_name='project_employees',
                                on_delete=models.CASCADE)
    employee = models.ForeignKey(to='employee.Employee', verbose_name=_('employee'), related_name='project_employees',
                                 on_delete=models.CASCADE)
    assigned_as = models.ForeignKey(to='employee.EmployeeType', verbose_name=_('assigned as'),
                                    related_name='project_employees', on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default=ACTIVE, verbose_name='status')

    def __str__(self):
        return str(self.project) + '-' + str(self.employee)

    def get_employee_name(self):
        return self.employee.user.get_full_name()

    class Meta:
        unique_together = ('project', 'employee')
