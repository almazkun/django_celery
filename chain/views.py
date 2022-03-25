from django.http import JsonResponse
from chain.tasks import add, power
from django.views.decorators.csrf import csrf_exempt
import traceback

# Create your views here.
@csrf_exempt
def run_task(request):
    try:
        if request.POST:
            a = int(request.POST.get("a"))
            b = int(request.POST.get("b"))
            task = add.delay(a, b)
            return JsonResponse({"task_id": task.id}, status=202)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "No data received"}, status=400)
