import ldap3
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ldap3 import Connection, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE
import os
import datetime
import pytz

from ldap3.core.exceptions import LDAPCursorAttributeError

from phonebook_django.settings import CACHE_TTL

AD_SEARCH_TREE = 'dc=gk,dc=local'
AD_SERVER = os.environ.get('AD_SERVER')
AD_USER = os.environ.get('AD_USER')
AD_PASSWORD = os.environ.get('AD_PASSWORD')
search_query = {
    'person_company': '(&(objectCategory=Person)(&(company=*)))',
    'person_company_active': '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803 := 2))(&(company=*)))'
}


def init_connection(search_string):
    conn = Connection(server=AD_SERVER, user=AD_USER, password=AD_PASSWORD)
    conn.bind()

    # (!(UserAccountControl:1.2.840.113556.1.4.803 := 2)) активные учетные записи
    conn.search(AD_SEARCH_TREE,
                search_string,
                SUBTREE,
                attributes=[ALL_ATTRIBUTES]
                )
    return conn.entries


def get_value(obj, field):
    try:
        result = getattr(obj, field).value
    except LDAPCursorAttributeError:
        result = ''
    return result


def index(request):
    selection = []
    all_users = init_connection(search_query['person_company_active'])
    sort = request.GET.get('sort')
    company = request.GET.get('company')

    if sort is None:
        sort = 'displayName'
    all_users.sort(key=lambda x: get_value(x, sort))

    for entry in all_users:
        if entry.company.value == company:
            selection.append(entry)

    if len(selection) == 0:
        context = {'entries': all_users, 'company': company}
    else:
        context = {'entries': selection, 'company': company}

    return render(request, 'phonebook/index.html', context)


@login_required()
def users(request):
    sort = request.GET.get('sort')
    selection = []
    all_users = init_connection(search_query['person_company'])
    utc = pytz.utc
    zero_lock_datetime = utc.localize(datetime.datetime(1601, 1, 1))

    print(zero_lock_datetime)

    if sort is None:
        sort = 'displayName'
    all_users.sort(key=lambda x: get_value(x, sort))

    for entry in all_users:
        # if hasattr(entry, 'lockoutTime') is False:
        if entry.userAccountControl == 514 or 66050:
            selection.append(entry)

    context = {
        'entries': selection,
        'all_users': all_users,
        'zero_lock_datetime': zero_lock_datetime,
    }
    return render(request, 'phonebook/users.html', context)


def status(request):
    conn = Connection(AD_SERVER, AD_USER, AD_PASSWORD)
    conn.bind()

    user = request.GET.get('user')
    state = request.GET.get('state')
    if state == 'disable':
        state = 514
    elif state == 'enable':
        state = 512
    else:
        pass

    conn.modify(user,
                {'userAccountControl': [(MODIFY_REPLACE, [state])]})
    print(conn.result)
    conn.unbind()

    return HttpResponseRedirect(reverse('phonebook:users'))
