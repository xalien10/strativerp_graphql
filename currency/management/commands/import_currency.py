import csv

from django.core.management import BaseCommand

from currency.models import Currency


class Command(BaseCommand):

    def ImportCurrency(self):
        with open('currencies.csv', encoding='utf-8') as currency_file:
            currencies = csv.reader(currency_file)
            for currency in currencies:
                title = currency[1]
                short_code = currency[2]
                print(title, short_code)
                try:
                    currency, created = Currency.objects.get_or_create(
                        title=title,
                        short_code=short_code,
                    )

                    if created:
                        currency.save()
                except Exception as ex:
                    print(str(ex))
                    msg = "\n\nSomething went wrong saving this Currency: {}\n{}".format(title, str(ex))
                    print(msg)
                    return msg

    def handle(self, *args, **options):
        """Called ImportCurrency function for import currency from currencies csv file."""
        self.ImportCurrency()
