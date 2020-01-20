from django.db import models
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    title = models.CharField(_('title'), max_length=100)
    short_code = models.CharField(_('short code'), max_length=3)
    icon = models.ImageField(verbose_name=_('icon'), upload_to='currency/', blank=True)
    icon1 = models.CharField(verbose_name=_('icon 1'), max_length=255, null=True, blank=True)
    icon2 = models.CharField(verbose_name=_('icon 2'), max_length=255, null=True, blank=True)
    icon3 = models.CharField(verbose_name=_('icon 3'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title + ' (' + self.short_code + ')'


class CurrencyCountry(models.Model):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    CURRENCY_TYPE = ((PRIMARY, _('Primary')), (SECONDARY, _('Secondary')))

    currency = models.ForeignKey(to='currency.Currency', verbose_name=_('currency'), related_name='currency_countries',
                                 on_delete=models.CASCADE)
    country = models.ForeignKey(to='contact.Country', verbose_name=_('country'), related_name='currency_countries',
                                on_delete=models.CASCADE)
    currencyType = models.CharField(verbose_name=_('currency_type'), choices=CURRENCY_TYPE, default=PRIMARY, max_length=255)

    def __str__(self):
        return self.currency.__str__() + '-' + self.country.name

    class Meta:
        unique_together = ('currency', 'country')
