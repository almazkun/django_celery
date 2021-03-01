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
        r = redis.Redis()
        data = {}
        for k in r.keys():
            if k.startswith(b"celery-"):
                task = json.loads(r.get(k).decode())
                data[task.get("task_id")] = task.get("result")

        return JsonResponse(data)
