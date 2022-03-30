# Create your models here.
class Data(models.Model):
    value = models.models.FloatField()


class Calculation(models.Model):
    OPERATIONS = (
        ('+', 'Add'),
        ('-', 'Subtract'),
        ('*', 'Multiply'),
        ('/', 'Divide'),
    )
    value_a = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='value_a')
    value_b = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='value_b')

    operation = models.ChoiceField(choices=OPERATIONS)


class CalculationResult(models.Model):
    calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
    result = models.models.FloatField()