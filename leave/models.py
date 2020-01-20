from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone
from django.utils.dates import MONTHS
from django.utils.translation import ugettext_lazy as _

from base.constants import LEAVE_TYPES, YEARS


class Leave(models.Model):
    REQUESTED = 1
    ALLOWED = 2
    DENIED = 3
    PROCESSED = 4
    LEAVE_STATUS = ((REQUESTED, _('Requested')), (ALLOWED, _('Allowed')), (DENIED, _('Denied')),
                    (PROCESSED, _('Processed')))

    employee = models.ForeignKey(to='employee.Employee', verbose_name=_('employee'), related_name='leaves',
                                 on_delete=models.CASCADE)
    leave_type = models.PositiveSmallIntegerField(verbose_name=_('leave type'), choices=LEAVE_TYPES)
    month = models.PositiveSmallIntegerField(verbose_name=_('month'), choices=MONTHS.items())
    year = models.PositiveSmallIntegerField(verbose_name=_('year'), choices=YEARS, default=datetime.datetime.now().year)
    start_date = models.DateField(verbose_name=_('start date'), default=timezone.now)
    end_date = models.DateField(verbose_name=_('end date'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), max_length=1000, null=True, blank=True)
    leave_status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=LEAVE_STATUS, default=REQUESTED)
    processed_by = models.ForeignKey(to='employee.Employee', verbose_name=_('processed by'),
                                     related_name='processed_by', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def duration(self):
        leave_start = self.start_date
        leave_end = self.end_date
        return (leave_end - leave_start).days

    def __str__(self):
        return str(self.leave_status)
