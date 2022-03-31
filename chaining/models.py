from django.db import models


# Create your models here.
class Data(models.Model):
    value = models.FloatField()


class Calculation(models.Model):
    OPERATIONS = (
        ("+", "Add"),
        ("-", "Subtract"),
        ("*", "Multiply"),
        ("/", "Divide"),
    )
    value_a = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="value_a")
    value_b = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="value_b")

    operation = models.CharField(choices=OPERATIONS, max_length=50)


class CalculationResult(models.Model):
    result = models.FloatField()
