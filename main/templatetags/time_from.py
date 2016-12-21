import datetime
import logging

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.dateparse import parse_datetime
from math import floor
from django.utils import timezone

register = Library()

logger = logging.getLogger('django.channels')


@register.filter
@stringfilter
def time_from(date):
    if date and date != "None":
        diff = (timezone.localtime(timezone.now()) - parse_datetime(date)).total_seconds() * 1000
        try:
            return int(diff)
        except ValueError:
            return None
    else:
        return None
