from celery import shared_task
from celery.utils.log import get_task_logger

from src.api.requests.sms_requests import send_sms

logger = get_task_logger(__name__)


@shared_task(name="broadcast_sms_task", priority=1)
def broadcast_sms_task(data: dict) -> None:
    phone_number = data["phone_number"]
    verify_code = data["verify_code"]
    text = f"Код подтверждения - {verify_code}"
    result = send_sms(text=text, phone_number=phone_number)
    logger.info(f"result of SMS sending - {result}")
