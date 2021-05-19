from datetime import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def format_mobile(string):
    return string[0:2] + ' ' + string[2:5] + ' ' + string[5:]


@register.filter
@stringfilter
def format_groups(string):
    return string[3:].split(',')[0]


@register.filter
@stringfilter
def format_description(string):  # добавить проверку строки
    string = string.split(' ')
    if len(string) != 3:
        return 'Неверный формат описания'
    else:
        string = 'Вход на ' + string[0] + ' ' + string[1] + ' в ' + string[2]
    return string


@register.filter
@stringfilter
def convert_str_date(value):
    return str(datetime.strptime(value, '%Y-%m-%d %H:%M:%S%z').strftime('%d.%m.%Y'))
