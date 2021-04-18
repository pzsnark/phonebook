# import ldap3
# from ldap3 import Connection, SUBTREE
# from django.shortcuts import render
# import os
# #
# #
# AD_SEARCH_TREE = 'dc=gk,dc=local'
# AD_SERVER = os.environ.get('AD_SERVER')
# AD_USER = os.environ.get('AD_USER')
# AD_PASSWORD = os.environ.get('AD_PASSWORD')
#
# def server_request():
#     server = ldap3.Server(AD_SERVER)
#     conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
#     conn.bind()
#
#     conn.search(AD_SEARCH_TREE,
#                 '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
#                 SUBTREE,
#                 attributes=['department', 'sAMAccountName', 'displayName', 'physicalDeliveryOfficeName',
#                             'telephoneNumber', 'mail', 'mobile', 'title', 'company', 'lastLogon']
#                 )
#     return conn.entries
#
#
# entries = server_request()
# print(type(entries))
# for entry in entries:
#     print(entry)


