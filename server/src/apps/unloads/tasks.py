from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q

logger = get_task_logger(__name__)


@shared_task(name="unload_fortochki_beat")
def unload_fortochki_beat() -> None:
    logger.info("Unloading fortochki...")
    return None


@shared_task(name="unload_starco_beat")
def unload_starco_beat() -> None:
    logger.info("Unloading starco...")
    return None
