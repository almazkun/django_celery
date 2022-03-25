from celery import shared_task


@shared_task
def add(a, b):
    return a + b


@shared_task
def power(c):
    return c ** c
