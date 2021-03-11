import ldap3
from ldap3 import Connection, SUBTREE
from .conf import *
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    server = ldap3.Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
    conn.bind()

    conn.search(AD_SEARCH_TREE,
                '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
                SUBTREE,
                attributes=['department', 'sAMAccountName', 'displayName', 'physicalDeliveryOfficeName',
                            'telephoneNumber', 'mail', 'mobile', 'title', 'company', 'lastLogon']
                )

    context = {
        'conn': conn.entries
    }
    return render(request, 'phonebook/index.html', context)
