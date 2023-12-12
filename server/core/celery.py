from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("leader_trade")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # "every_hour": {"task": "update_api_client_beat", "schedule": crontab(hour="1")},
    # "fortochki_tire_upload_beat_every_minute": {
    #     "task": "fortochki_tire_upload_beat",
    #     "schedule": crontab(minute="*/1"),
    # },
    # "fortochki_rim_upload_every_minute": {
    #     "task": "fortochki_rim_upload_beat",
    #     "schedule": crontab(minute="*/1"),
    # },
    # "starco_get_products_beats_every_min": {
    #     "task": "starco_get_products_beats",
    #     "schedule": crontab(minute="*/1"),
    # },
    # "starco_get_current_stock_beat_every_min": {
    #     "task": "starco_get_current_stock_beat",
    #     "schedule": crontab(minute="*/1"),
    # },
}
