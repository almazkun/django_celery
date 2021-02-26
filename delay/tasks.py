from celery import shared_task


@shared_task
def power(x, y):
    return x ** y
