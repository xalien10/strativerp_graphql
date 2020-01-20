from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from cron import aps_scheduler_job
        aps_scheduler_job.start()
