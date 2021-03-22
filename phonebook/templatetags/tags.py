from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def format_mobile(string):
    return string[0:2] + ' ' + string[2:5] + ' ' + string[5:]
