from django import template
from django.template.defaultfilters import stringfilter
from loguru import logger

register = template.Library()
logger.add('debug.log', format='{time:DD-MM-YYYY HH:mm} {level} {message}', level='DEBUG', rotation='100 KB', compression='zip')


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
        logger.warning('Invalid description format')
        return 'Неверный формат описания'
    else:
        string = 'Вход на ' + string[0] + ' ' + string[1] + ' в ' + string[2]
    return string
