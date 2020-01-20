from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.constants import TIME_ESTIMATION_TYPE, MONTHLY


class Salary(models.Model):
    employee = models.ForeignKey(to='employee.Employee', verbose_name=_('employee'), related_name='salaries',
                                 on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name=_('amount'), max_digits=10, decimal_places=2)
    salary_freq = models.CharField(verbose_name=_('salary frequency'), max_length=50, choices=TIME_ESTIMATION_TYPE,
                                   default=MONTHLY)
    description = models.TextField(verbose_name=_('description'), max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.amount)

    def get_hourly_salary(self):
        salary = 0
        if self.salary_freq == 'hourly':
            salary = self.amount
        elif self.salary_freq == 'daily':
            salary = self.amount / 5
        elif self.salary_freq == 'weekly':
            salary = self.amount / 37.5
        elif self.salary_freq == 'weekly':
            salary = self.amount / 150
        return salary
