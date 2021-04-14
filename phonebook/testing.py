import ldap3
from ldap3 import Connection, SUBTREE, MODIFY_REPLACE
import os

from ldap3.core.exceptions import LDAPCommunicationError

AD_SEARCH_TREE = 'dc=gk,dc=local'
AD_SERVER = os.environ.get('AD_SERVER')
AD_USER = os.environ.get('AD_USER')
AD_PASSWORD = os.environ.get('AD_PASSWORD')


server = ldap3.Server(AD_SERVER)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD)

try:
    conn.bind()
except LDAPCommunicationError:
    print('Ошибка подключения')

# add function
# conn.modify('cn=Филиппов Константин Николаевич,ou=IT,dc=gk,dc=local',
#             {'telephoneNumber': [(MODIFY_REPLACE, ['800'])]})
# print(conn.result)

# search function
conn.search(AD_SEARCH_TREE,
            '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(department=IT)))',
            SUBTREE,
            attributes=[ldap3.ALL_ATTRIBUTES]
            )
# print(conn.entries)


# def sort(self, sort_value):
#     try:
#         return self.employee_list.sort(key=lambda x: getattr(x, sort_value))
#     except AttributeError:
#         print(f'Object has no attribute {sort_value}')


# conn.entries.sort(key=lambda x: x.name.value)

for entry in conn.entries:
    print(entry)

conn.unbind()
