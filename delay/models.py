from django.db import models

# Create your models here.
class SomeTask(models.Model):
    task_id = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]
