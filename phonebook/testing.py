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


# function of add
# conn.modify('cn=Филиппов Константин Николаевич,ou=IT,dc=gk,dc=local',
#             {'telephoneNumber': [(MODIFY_REPLACE, ['800'])]})
# print(conn.result)

# search function
conn.search(AD_SEARCH_TREE,
            '(&(department=IT))',
            SUBTREE,
            attributes=[ldap3.ALL_ATTRIBUTES]
            )
# print(conn.entries)

conn.entries.sort(key=lambda x: x.name.value)

selection = []
for entry in conn.entries:
    if entry.userAccountControl.value == 66050:
        selection.append(entry)
print(len(selection), selection)

conn.unbind()
