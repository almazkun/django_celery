import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from settings.celery_rabbitmq import app_rabbitmq
from settings.celery_redis import app_redis


# Create your views here.
@csrf_exempt
def run_task(request):
    try:
        if request.POST:
            a = int(request.POST.get("a"))
            b = int(request.POST.get("b"))

            t_1 = app_redis.send_task("settings.celery_redis.add", args=[a, b])
            t_2 = app_redis.send_task("settings.celery_redis.power", args=[b])
            t_3 = app_rabbitmq.send_task(
                "settings.celery_rabbitmq.save_to_db", args=[{"power": b}]
            )

            return JsonResponse({"task_ids": [t_1.id, t_2.id, t_3.id]})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "No data received"}, status=400)
