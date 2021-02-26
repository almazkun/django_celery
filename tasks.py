from celery import Celery


app = Celery("tasks", broker="redis://:some_password@localhost")


@app.task
def add(x, y):
    return x ** y
