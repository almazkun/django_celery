import traceback

from celery import chain
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import settings.celery_redis


# Create your views here.
@csrf_exempt
def run_task(request):
    try:
        if request.POST:
            a = int(request.POST.get("a"))
            b = int(request.POST.get("b"))
            mt_task = chain(
                settings.celery_redis.add.s(a, b),
                settings.celery_redis.power.s(),
            ).apply_async()
            return JsonResponse({"task_id": mt_task.id})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "No data received"}, status=400)
