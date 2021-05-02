import datetime

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value < 1900 or value > datetime.datetime.now().year:
        raise ValidationError('It\'s is not a correct year!')
