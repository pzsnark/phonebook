import ldap3
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ldap3 import Connection, Server, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE
import os
import datetime
import pytz
from .forms import CreateADUserForm
from .utils import get_value, clear_dict

from ldap3.core.exceptions import LDAPCursorAttributeError

from phonebook_django.settings import CACHE_TTL

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


def index(request):
    selection = []
    all_users = init_connection(search_query['person_company_active']).entries
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
    all_users = init_connection(search_query['person_company']).entries
    utc = pytz.utc
    zero_lock_datetime = utc.localize(datetime.datetime(1601, 1, 1))

    print(zero_lock_datetime)

    if sort is None:
        sort = 'displayName'
    all_users.sort(key=lambda x: get_value(x, sort))

    for entry in all_users:
        if entry.userAccountControl == 514 or 66050:
            selection.append(entry)

    context = {
        'entries': selection,
        'all_users': all_users,
        'zero_lock_datetime': zero_lock_datetime,
    }
    return render(request, 'phonebook/users.html', context)


@login_required()
def status(request):
    conn = init_connection(search_query['person_company'])

    user = request.GET.get('user')
    state = request.GET.get('state')
    field = 'userAccountControl'

    if state == 'disable':
        state = 514
    elif state == 'enable':
        state = 512
    elif state == 'unlock':
        field = 'lockoutTime'
        state = 0

    conn.modify(user,
                {field: [(MODIFY_REPLACE, [state])]})
    print(conn.result)
    conn.unbind()

    return HttpResponseRedirect(reverse('phonebook:users'))


@login_required()
def create_ad_user(request):
    if request.method == 'POST':
        form = CreateADUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            middle_name = form.cleaned_data.get('middle_name')
            title = form.cleaned_data.get('title')
            department = form.cleaned_data.get('department')
            location = form.cleaned_data.get('location')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            mobile = form.cleaned_data.get('mobile')
            company = form.cleaned_data.get('company')
            require_pass_change = 0

            account_name = f'{last_name}.{first_name[:1]}{middle_name[:1]}'
            display_name = f'{last_name} {first_name} {middle_name}'
            dn = f'CN={display_name},OU={company},DC=gk,DC=local'
            domain = 'gk.local'
            userpass = 'Qq123456'
            fields = {
                'sAMAccountName': account_name,
                'userPrincipalName': f'{account_name}@{domain}',
                'givenName': first_name,
                'sn': last_name,
                'displayName': display_name,
                'title': title,
                'department': department,
                'physicalDeliveryOfficeName': location,
                'mail': email,
                'telephoneNumber': phone,
                'mobile': mobile,
                'company': company,
            }

            clear_dict(fields)
            print(fields)

            conn = init_connection(search_query['person_company_active'])

            # create user
            conn.add(dn, ['organizationalPerson', 'person', 'top', 'user'], fields)
            result = conn.result
            # set password
            conn.extend.microsoft.modify_password(dn, 'Qq123456')
            # enable user & require change password
            conn.modify(dn, {'userAccountControl': [('MODIFY_REPLACE', 512)], 'pwdLastSet': [('MODIFY_REPLACE', 0)]})

            # conn.unbind()
            return render(request, 'phonebook/create_ad_user.html',
                          {'result': result['description'], 'account_name': account_name, 'form': form})
    else:
        form = CreateADUserForm()

    return render(request, 'phonebook/create_ad_user.html', {'form': form})
