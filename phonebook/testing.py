import ldap3
from ldap3 import Connection, Server, SUBTREE, ALL_ATTRIBUTES, Entry, Reader, ObjectDef, AttrDef
import os
import json
from types import SimpleNamespace
from collections import namedtuple

from models import Entry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phonebook.settings')

AD_SEARCH_TREE = 'dc=gk,dc=local'
AD_SERVER = os.environ.get('AD_SERVER')
AD_USER = os.environ.get('AD_USER')
AD_PASSWORD = os.environ.get('AD_PASSWORD')
SERVER = Server(AD_SERVER, port=636, use_ssl=True)
search_query = {
    'person_company': '(&(objectCategory=Person)(&(company=*)))',
    'person_company_active': '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803 := 2))(&(company=*)))'
}


def init_connection(search_string):
    conn = Connection(SERVER, user=AD_USER, password=AD_PASSWORD)
    conn.bind()

    # (!(UserAccountControl:1.2.840.113556.1.4.803 := 2)) активные учетные записи
    conn.search(AD_SEARCH_TREE,
                search_string,
                SUBTREE,
                attributes=['cn', 'displayName', 'memberOf']
                )
    return conn


dictionary = {'name': 'Bob', 'age': '12'}
print(dictionary)
obj_name = namedtuple('Struct', dictionary.keys())(*dictionary.values())
print(obj_name)

response = init_connection('(physicalDeliveryOfficeName=207)')
response_json = response.response_to_json()
str_json = json.loads(response_json)

person_list = []
for entry in str_json['entries']:
    person = entry['attributes']
    person = namedtuple('Struct', person.keys())(*person.values())
    person_list.append(person)

for person in person_list:
    print(person.displayName)


# conn = Connection(SERVER, user=AD_USER, password=AD_PASSWORD)
# conn.bind()
#
# objectdef = ObjectDef('organizationalPerson', schema=SERVER.schema)
# print(objectdef)
#
# base = 'dc=gk,dc=local'
#
# cursor = Reader(conn, objectdef, base)
# print(cursor)
#
# dn = 'CN=Филиппов Константин Николаевич,OU=IT,DC=gk,DC=local'
#
# person = Entry(dn, cursor)
# print(person.entry_to_json())
#
# conn.unbind()
