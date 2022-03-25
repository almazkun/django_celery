# Django and Celery
and Radis Waiting...

## Docs

1. https://testdriven.io/blog/django-and-celery/

## 1. Setup
1. `mkdir ~/dj_celery`
2. `cd ~/dj_celery`
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
7. nano settings/\_\_init\_\_.py
```py
# settings/__init__.py
from .celery import app as celery_app


__all__ = ("celery_app",)
```
8. nano settings/settings.py
```py
# settings/settings.py
# append following:
...

CELERY_BROKER_URL = "redis://:redis_password@:6379"
CELERY_RESULT_BACKEND = "redis://:redis_password@:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Oslo"


INSTALLED_APPS += "delay"
ALLOWED_HOSTS += "*"
```
9. 
```
docker run -d \
  -h redis \
  -v redis-data:/redis_data \
  -p 6379:6379 \
  --name redis \
  --restart always \
  redis:6 /bin/sh -c 'redis-server --requirepass redis_password'
```

10. `python manage.py runserver`

## 2. Django tasks, views, and urls
1. `nano delay/tasks.py`
```py
# delay/tasks.py
from celery import shared_task


@shared_task
def power(x: int, y: int) -> int:
    return x ** y
```
2. `nano delay/views.py`
```py
# delay/views.py
import redis
import json

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from delay.tasks import power


@method_decorator(csrf_exempt, name="dispatch")
class JustView(View):
    def post(self, request):
        task = power.delay(x=int(request.POST.get("x")), y=int(request.POST.get("y")))

        return JsonResponse({"task_id": task.id})

    def get(self, request):
        r = redis.Redis(password="redis_password")
        data = {}
        for k in r.keys():
            if k.startswith(b"celery-"):
                task = json.loads(r.get(k).decode())
                data[task.get("task_id")] = task.get("result")

        return JsonResponse(data)
```
3. `nano settings/urls.py`
```py
# settings/urls.py
# append following:

urlpatterns += path("", JustView.as_view(), name="home")
```
5. `celery -A settings worker -l info`
6. `curl -d "x=10&y=64" -X POST http://localhost:8000`
7. `curl http://localhost:8000`

## 3. Celery in the Background
1. `sudo apt-get install supervisor`
2. `mkdir /var/log/celery/`
3. `touch /var/log/celery/delay.log`
4. `nano /etc/supervisor/conf.d/celery.conf`
```conf
; /etc/supervisor/conf.d/celery.conf
[program:celery]
command=pypenv run celery -A settings worker -l info
directory=~/dj_celery
numprocs=1
stdout_logfile=/var/log/celery/delay.log
stderr_logfile=/var/log/celery/delay.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs = 600
killasgroup=true
```
5. `sudo supervisorctl reread`
6. `sudo supervisorctl update`
