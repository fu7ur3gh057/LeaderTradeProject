from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from src.apps.unloads.models import UnloadScheduler
from src.other.enums import TaskStatus


@receiver(signal=post_save, sender=UnloadScheduler)
def create_or_update_unload(
    sender, instance: UnloadScheduler, created, **kwargs
) -> None:
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = instance.interval_schedule
            instance.task.save()
