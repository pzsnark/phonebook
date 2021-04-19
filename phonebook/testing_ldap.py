import ldap
import os

AD_SERVER = os.environ.get('AD_SERVER')
AD_USER = os.environ.get('AD_USER')
AD_PASSWORD = os.environ.get('AD_PASSWORD')


conn = ldap.initialize('ldap://dc1.gk.local', bytes_mode=False)
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s('ldap-bot', '12345678')

basedn = 'ou=IT,dc=gk,dc=local'
scope = ldap.SCOPE_SUBTREE
searchFilter = '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))'
attrlist = ['sAMAccountName', 'mail']

users = conn.search_s(basedn, scope, searchFilter, attrlist)

# for user in users:
#     string = ((user[1]).get('sAMAccountName')[0])


class Employee:

    def __init__(self):
        self.__fields = attrlist

    def __getattr__(self, field_name):
        if field_name in self.__fields:
            return self.__fields[field_name]
        else:
            return self.__dict__.get(field_name)

    # def import_users(self):
    #     for user in users:
    #         Employee


user_object = Employee
print(user_object)
