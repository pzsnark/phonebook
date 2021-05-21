from collections import namedtuple
from .models import Company

from ldap3.core.exceptions import LDAPCursorAttributeError


# получаем значение из объекта
def get_value(obj, field):
    try:
        result = getattr(obj, field)
    except AttributeError:
        result = ''
    return result


# очищаем словарь от ключей с пустыми значениями
def clear_dict(dictionary):
    dict_copy = dictionary.copy()
    for key in dict_copy:
        if not dictionary.get(key):
            dictionary.pop(key)
    return dictionary


def clear_dict_none(dictionary):
    """Чистим словарь от ключей со значением None"""
    dict_copy = dictionary.copy()
    for key in dict_copy:
        if dictionary.get(key) is None:
            dictionary.pop(key)
    return dictionary


# создаем объект из списка
def list_to_object(array):
    obj = namedtuple('PersonObject', array.keys())(*array.values())
    return obj


def company_list():
    all_entries = list(Company.objects.values())
    entries = [(d['slug'], d['name']) for d in all_entries]
    return entries
