from __future__ import absolute_import, unicode_literals
import os
import datetime
import pytz
from celery import Celery
from celery.schedules import crontab
import configurations


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corner_test.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")


configurations.setup()


class CelerySettings:
    accept_content = ["json"]
    CELERY_ENABLE_UTC = True
    task_serializer = "json"
    task_always_eager = True
    task_eager_propagates = True
    task_ignore_result = os.getenv("CELERY_IGNORE_RESULT", "True")
    task_store_errors_even_if_ignored = True
    task_acks_late = True
    CELERY_TASK_REJECT_ON_WORKER_LOST = True
    result_backend = os.getenv("CELERY_RESULT_BACKEND_URL", "redis://redis:6379/0")
    result_serializer = "json"
    result_expires = 60 * 60 * 24
    task_default_queue = "celery"
    task_default_exchange = task_default_queue
    task_default_routing_key = task_default_queue
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    broker_pool_limit = 10
    broker_connection_max_retries = 0
    broker_heartbeat = None
    worker_lost_wait = 20
    worker_hijack_root_logger = os.getenv("CELERYD_HIJACK_ROOT_LOGGER", "False")
    worker_pool_restarts = True
    SLACK_API_KEY = os.getenv("SLACK_API_KEY")
    timezone = "America/Santiago"


settings = CelerySettings()

app = Celery("corner_test")
app.config_from_object(settings)
from django.conf import settings

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "send_daily_menu_reminder": {
        "task": "corner_test.apps.menus.tasks.send_today_menu",
        "schedule": crontab(minute=0, hour=8),
    },
    "save_orders": {
        "task": "corner_test.apps.menus.tasks.save_messages",
        "schedule": crontab(minute=0, hour=11),
    },
}
