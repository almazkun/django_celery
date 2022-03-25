import datetime

from celery import Celery
from django.conf import settings


app = Celery(
    "tasks",
    broker="amqp://remote_guest:remote_guest@rabbitmq:5672/",
    backend="amqp",
)
app.conf.update(
    result_expires=datetime.timedelta(days=5),
    result_persistent=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    worker_pool_restarts=True,
    # worker_prefetch_multiplier=1, # NOTE: this breaks auto-scaling
    task_acks_late=False,
    task_track_started=True,
    worker_max_tasks_per_child=1,
    task_reject_on_worker_lost=False,
    broker_pool_limit=None,
)
