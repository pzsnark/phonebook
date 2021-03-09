import ldap3
from ldap3 import Connection, SUBTREE
from conf import *

server = ldap3.Server(AD_SERVER)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
conn.bind()

conn.search(AD_SEARCH_TREE, '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
            SUBTREE,
            attributes=['cn', 'department', 'sAMAccountName', 'displayName', 'telephoneNumber',
                        'ipPhone', 'title', 'manager', 'company', 'lastLogon']
            )

print(conn.entries)

# for entry in conn.entries:
#     print(entry.cn, entry.company)

# '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
