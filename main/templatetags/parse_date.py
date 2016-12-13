import datetime

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.dateparse import parse_datetime

register = Library()


@register.filter
@stringfilter
def parse_date(date_string):
    """
    Return a datetime corresponding to date_string, parsed according to format.

    For example, to re-display a date string in another format::

        {{ "01/01/1970"|parse_date:"%m/%d/%Y"|date:"F jS, Y" }}

    """
    try:
        return parse_datetime(date_string)
    except ValueError:
        return None
