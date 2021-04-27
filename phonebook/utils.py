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

#
# def format_groups(entries):
#     groups = []
#     for entry in entries:
#         for group in entry.memberOf:
#             group = groups.append(group[3:].split(',')[0])
#     return groups

# if 'memberOf' in i[1]:
#           g=[]
#           for z in i[1]['memberOf']:
#               z=z.decode('utf8')
#               z=z[3:]
#               z=z.split(',')[0]
#               g.append(z)
#           user['memberOf']=g
