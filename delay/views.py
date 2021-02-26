from django.views.generic import View
from django.http import JsonResponse

from delay.models import SomeTask
from delay.tasks import power


class JustView(View):
    def get(self, request, *args, **kwargs):
        x = kwargs.get("x")
        y = kwargs.get("y")
        result = power.delay(x, y)
        st = SomeTask.objects.create()

        return JsonResponse({"wait": "please"})
