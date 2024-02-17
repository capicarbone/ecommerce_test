from decimal import Decimal
from typing import Any


def is_valid_percentage(value: Any):
    return isinstance(value, Decimal) and value > Decimal("0") and value <= Decimal("1")


def is_valid_amount(value: Any):
    return isinstance(value, Decimal) and value >= Decimal("0")
