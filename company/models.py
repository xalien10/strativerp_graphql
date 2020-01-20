from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class Company(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    contact = models.ForeignKey(to='contact.Contact', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(to='contact.Address', on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.ImageField(verbose_name=_('logo'), upload_to='company/', null=True, blank=True)
    website = models.URLField(verbose_name=_('website'), null=True, blank=True)
    currency = models.ForeignKey(to='currency.Currency', verbose_name=_('currency'), related_name='companies',
                                 on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
