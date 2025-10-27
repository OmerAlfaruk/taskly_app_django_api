from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BackgroundJobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'background_jobs'

    def ready(self):
        from background_jobs.task import calculate_house_status
        from background_task.tasks import Task as BT

        def schedule_tasks(sender, **kwargs):
            if not BT.objects.filter(verbose_name="calculate_house_status").exists():
                calculate_house_status(repeat=BT.DAILY, verbose_name='calculate_house_status', priority=0)

        # Register the function to run after migrations
        post_migrate.connect(schedule_tasks, sender=self)
