import ldap3
from ldap3 import Connection, SUBTREE
from django.shortcuts import render

AD_SERVER = 'dc2.gk.local'
AD_USER = 'ldap-bot@gk.local'
AD_PASSWORD = '12345678'
AD_SEARCH_TREE = 'dc=gk,dc=local'


def server_request():
    server = ldap3.Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
    conn.bind()

    conn.search(AD_SEARCH_TREE,
                '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
                SUBTREE,
                attributes=['department', 'sAMAccountName', 'displayName', 'physicalDeliveryOfficeName',
                            'telephoneNumber', 'mail', 'mobile', 'title', 'company', 'lastLogon']
                )
    return conn.entries


entries = server_request()
print(type(entries))
for entry in entries:
    print(entry)
