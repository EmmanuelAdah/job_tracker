from django.apps import AppConfig


class JobConfig(AppConfig):
    name = 'job'

    def ready(self):
        import job.signals  # This connects the logic when Django starts
