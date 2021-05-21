from collections import namedtuple
from smtplib import SMTPAuthenticationError, SMTPDataError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ldap3 import Connection, Server, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE
import os
import datetime
import pytz
from .forms import CreateForm
from .utils import get_value, clear_dict, list_to_object
from django.core.mail import send_mass_mail
from actionlog.utils import get_actionlog
from .models import Entry
import json
from phonebook_django.settings import CACHE_TTL, RECIPIENT_LIST

from .conf import ATTRIBUTES, AD_USER, AD_PASSWORD, AD_SERVER

AD_SEARCH_TREE = 'dc=gk,dc=local'
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
                attributes=ATTRIBUTES
                )
    return conn


def index(request):
    person_list_filter_by_company = []
    # all_ad_users = init_connection(search_query['person_company_active']).entries

    response = init_connection(search_query['person_company_active'])
    response_json = response.response_to_json()
    ad_person_list = json.loads(response_json)

    person_list = []

    # добавляем пользователй из AD
    for entry in ad_person_list['entries']:
        ad_person = entry['attributes']
        clear_dict(ad_person)
        ad_person = list_to_object(ad_person)
        person_list.append(ad_person)

    # добавляем пользователей из DB
    model_person_list = Entry.model_to_json()
    for model_person in model_person_list:
        clear_dict(model_person)
        model_person = list_to_object(model_person)
        person_list.append(model_person)

    sort = request.GET.get('sort')
    company = request.GET.get('company')
    utc = pytz.utc
    zero_lock_datetime = utc.localize(datetime.datetime(1601, 1, 1))

    if sort is None:
        sort = 'displayName'
    person_list.sort(key=lambda x: get_value(x, sort))

    for person in person_list:
        if person.company == company:
            person_list_filter_by_company.append(person)

    context = {
        'company': company,
        'zero_lock_datetime': zero_lock_datetime,
    }

    context.update(get_actionlog())

    if len(person_list_filter_by_company) == 0:
        context['entries'] = person_list
    else:
        context['entries'] = person_list_filter_by_company

    return render(request, 'phonebook/index.html', context)


@login_required()
def users(request):
    sort = request.GET.get('sort')
    selection = []
    all_users = init_connection(search_query['person_company']).entries
    utc = pytz.utc
    zero_lock_datetime = utc.localize(datetime.datetime(1601, 1, 1))

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
    conn.unbind()

    return HttpResponseRedirect(reverse('phonebook:index'))


@login_required()
def create_ad_user(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
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

            account_name = f'{last_name}.{first_name[:1]}{middle_name[:1]}'
            display_name = f'{last_name} {first_name} {middle_name}'
            dn = f'CN={display_name},OU={company},DC=gk,DC=local'
            domain = 'gk.local'
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

            # clear_dict(fields)

            conn = init_connection(search_query['person_company_active'])

            # create user
            conn.add(dn, ['organizationalPerson', 'person', 'top', 'user'], fields)
            result = conn.result
            # set password
            conn.extend.microsoft.modify_password(dn, 'Qq123456')
            # enable user & require change password
            conn.modify(dn, {'userAccountControl': [('MODIFY_REPLACE', 512)], 'pwdLastSet': [('MODIFY_REPLACE', 0)]})

            result_send_mail = int()
            message_text = f'Создан пользователь {display_name},' \
                           f' с почтовым адресом {email}.' \
                           f' Телефон: {phone},' \
                           f' Мобильный: {mobile}'
            message = ('Справочник пользователей', message_text, 'it@avsst.ru', RECIPIENT_LIST)
            if result['description'] == 'success':
                try:
                    result_send_mail = send_mass_mail((message,), fail_silently=False)
                except SMTPAuthenticationError as error:
                    result_send_mail = error
                except SMTPDataError as error:
                    result_send_mail = error

            conn.unbind()
            return render(request, 'phonebook/create_entry.html',
                          {
                              'result': result['description'],
                              'result_send_mail': result_send_mail,
                              'account_name': account_name,
                              'form': form,
                          })
    else:
        form = CreateForm()

    return render(request, 'phonebook/create_entry.html', {'form': form})


# class CreateEntry(View):
#     template_name = 'phonebook/create_entry.html'
#     form = CreateForm
#
#     def get(self, request):
#         context = {'form': self.form}
#         return render(request=request, template_name=self.template_name, context=context)
#
#     def post(self, request):
#         form = CreateForm(data=request.POST)
#         registered = False
#         if form.is_valid():
#             entry = Entry
#             entry.first_name = form.cleaned_data.get('first_name')
#             entry.last_name = form.cleaned_data.get('last_name')
#             entry.middle_name = form.cleaned_data.get('middle_name')
#             entry.title = form.cleaned_data.get('title')
#             entry.department = form.cleaned_data.get('department')
#             entry.location = form.cleaned_data.get('location')
#             entry.email = form.cleaned_data.get('email')
#             entry.phone = form.cleaned_data.get('phone')
#             entry.mobile = form.cleaned_data.get('mobile')
#             entry.company = form.cleaned_data.get('company')
#
#             entry.save()
#             registered = True
#             return render(request, 'phonebook/create_entry.html', {'registered': registered})
#         else:
#             return render(request, 'phonebook/create_entry.html',
#                           {'form': form, 'registered': registered})
