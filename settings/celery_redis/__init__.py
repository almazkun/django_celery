import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app_redis = Celery(
    settings.REDIS_CELERY_APP_NAME,
    broker=settings.REDIS_CELERY_BROKER_URL,
    backend=settings.REDIS_CELERY_RESULT_BACKEND,
)

app_redis.conf.update(
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
)


@app_redis.task
def add(x: int, y: int) -> int:
    return x + y


@app_redis.task
def power(c: int) -> dict:
    return {"power": c ** 2}
