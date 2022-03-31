import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app_rabbitmq = Celery(
    settings.RABBITMQ_CELERY_APP_NAME,
    broker=settings.RABBITMQ_CELERY_BROKER_URL,
    backend=settings.RABBITMQ_CELERY_RESULT_BACKEND,
)

app_rabbitmq.conf.update(
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
)


@app_rabbitmq.task
def save_to_db(data: dict) -> dict:
    from chaining.models import CalculationResult

    result = CalculationResult(result=data["power"]).save()
