from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Initialization has started.....')
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='Employee')
        self.stdout.write('Groups created .....')
