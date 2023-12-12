from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from src.apps.unloads.models import Unload
from src.other.enums import TaskStatus


@receiver(signal=post_save, sender=Unload)
def create_or_update_unload(sender, instance: Unload, created, **kwargs) -> None:
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.save()


# @receiver(signal=pre_delete, sender=Unload)
# def delete_periodic_task(sender, instance: Unload, using, **kwargs) -> None:
#     instance.terminate()
