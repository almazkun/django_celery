# Django and Celery
and Radis Waiting...

## Setup
1. `mkdir dj_celery`
2. `cd dj_celery`
3. `pipenv install django "celery[redis]"`
4. `django-admin startproject settings .`
5. `python3 manage.py startapp delay`
6. `nano settings/celery.py`
```py
# settings/celery.py
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app = Celery("settings")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
```
7. nano settings/__init__.py
```
# settings/__init__.py
from .celery import app as celery_app


__all__ = ("celery_app",)
```
8. nano settings/settings.py
```py
CELERY_BROKER_URL = 'redis://localhost'
```
9.`docker run --name redis -e ALLOW_EMPTY_PASSWORD=yes -p 6379:6379 -d redis:buster`
10. `python manage.py runserver`
