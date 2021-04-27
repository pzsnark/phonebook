from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter
@stringfilter
def format_mobile(string):
    return string[0:2] + ' ' + string[2:5] + ' ' + string[5:]


@register.filter
@stringfilter
def format_groups(string):
    return string[3:].split(',')[0]
