from ldap3.core.exceptions import LDAPCursorAttributeError


# получаем значение из объекта
def get_value(obj, field):
    try:
        result = getattr(obj, field).value
    except LDAPCursorAttributeError:
        result = ''
    return result


# очищаем словарь от ключей с пустыми значениями
def clear_dict(dictionary):
    dict_copy = dictionary.copy()
    for key in dict_copy:
        if dictionary.get(key) == '':
            dictionary.pop(key)
    return dictionary
