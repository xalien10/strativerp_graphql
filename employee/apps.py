from django.apps import AppConfig


class StaffConfig(AppConfig):
    name = 'employee'

    def ready(self):
        pass
# import employee.signals
