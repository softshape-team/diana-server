from django.utils import timezone
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


@deconstructible
class FutureDateTimeValidator:
    """
    Validate a datetime field,
    return True if the datetime in the future, False otherwise.
    """

    msg = "Enter a valid datetime, the datetime should not be passed."

    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg

    def __call__(self, value):
        if value < timezone.now():
            raise ValidationError(self.msg)
