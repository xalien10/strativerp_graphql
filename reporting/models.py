from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class ReportedHour(BaseModel):
    project_employee = models.ForeignKey('project.ProjectEmployee', verbose_name=_('project'),
                                         related_name='reported_hours',
                                         on_delete=models.CASCADE)
    date = models.DateField(verbose_name=_('date'), default=timezone.now)
    hours = models.DecimalField(verbose_name=_('hours'), max_digits=10, decimal_places=2)
    minute = models.DecimalField(verbose_name=_('minute'), max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField(verbose_name=_('description'), max_length=1000, null=True, blank=True)
    income = models.DecimalField(verbose_name=_('income'), max_digits=10, decimal_places=2, default=0.0,
                                 null=True, blank=True)
    is_billable = models.BooleanField(verbose_name=_('is billable'), default=True)
    cost = models.DecimalField(verbose_name=_('cost'), max_digits=10, decimal_places=2, default=0.0,
                               null=True, blank=True)
    profit = models.DecimalField(verbose_name=_('profit'), max_digits=10, decimal_places=2, default=0.0,
                                 null=True, blank=True)

    def __str__(self):
        return str(self.project_employee) + '-' + str(self.hours)

    def get_time(self):
        return self.hours + self.minute / 60

    def get_username(self):
        return self.project_employee.employee.user.get_full_name()

    def get_email(self):
        return self.project_employee.employee.email

    def get_project_name(self):
        return self.project_employee.project.name

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('project_employee', 'date', 'is_billable')
