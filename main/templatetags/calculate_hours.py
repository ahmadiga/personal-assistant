import datetime

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.dateparse import parse_datetime
from math import floor

register = Library()


@register.filter
@stringfilter
def calculate_hours(date_string):
    date_string = int(date_string)
    seconds = floor((date_string / 1000) % 60)
    minutes = floor((date_string / (1000 * 60)) % 60)
    hours = floor((date_string / (1000 * 60 * 60)))
    try:
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    except ValueError:
        return None
