import logging

from chain.models import Calculation, Data

logger = logging.getLogger(__name__)


def save_calculation(a, b, operation):
    logger.debug(f"Saving calculation {a} {operation} {b}")

    value_a = Data(value=a).save()
    value_b = Data(value=b).save()

    calculation = Calculation(
        value_a=value_a, value_b=value_a, operation=operation
    ).save()


def performe_calculation(calculation_pk: str):
    logger.debug(f"Performing calculation {calculation_pk}")

    calculation = Calculation.objects.get(pk=calculation_pk)
    a = calculation.value_a.value
    b = calculation.value_b.value
    operation = calculation.operation

    try:
        if operation == "+":
            return a + b
        elif operation == "-":
            return a - b
        elif operation == "*":
            return a * b
        elif operation == "/":
            return a / b
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"Error performing calculation: {e}")
    else:
        raise Exception("Invalid operation")


def save_result_of_calculation(calculation_pk: str):
    logger.debug(f"Saving result of calculation {calculation_pk}")

    calculation = Calculation.objects.get(pk=calculation_pk)
