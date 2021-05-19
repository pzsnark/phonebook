import ldap3
from ldap3 import Connection, Server, SUBTREE, ALL_ATTRIBUTES, Entry, Reader, ObjectDef, AttrDef
import os
import json
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
                attributes=[ALL_ATTRIBUTES]
                )
    return conn


example = init_connection('(&(objectCategory=Person)(&(company=PNL)))')
person_json = example.response_to_json()
print(type(person_json))

entries = json.loads(person_json)
for entry in entries['entries']:
    print(entry['attributes'].keys())

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
