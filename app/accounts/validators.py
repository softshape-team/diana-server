from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class BothIncludedRangeValidator:
    """
    Validate range (a, b) the value should be between a and b both included
    """

    msg = "Enter a valid range"

    def __init__(self, start: float, end: float, msg=None):
        self.start = start
        self.end = end

        if msg is not None:
            self.msg = msg

    def __call__(self, value: float):
        if value < self.start or value > self.end:
            raise ValidationError(self.msg)
