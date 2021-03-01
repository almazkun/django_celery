from celery import shared_task


@shared_task
def power(x: int, y: int) -> int:
    return x ** y
