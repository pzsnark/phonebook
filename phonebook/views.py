from smtplib import SMTPAuthenticationError, SMTPDataError
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.views.decorators.cache import cache_page
from ldap3 import Connection, Server, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE
import os
import datetime
import pytz
from .forms import CreateForm
from .utils import get_value, clear_dict
from django.core.mail import send_mass_mail
from actionlog.utils import get_actionlog
from .models import Entry, Company


from phonebook_django.settings import CACHE_TTL, RECIPIENT_LIST

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
    all_ad_users = init_connection(search_query['person_company_active']).entries

    sort = request.GET.get('sort')
    company = request.GET.get('company')
    utc = pytz.utc
    zero_lock_datetime = utc.localize(datetime.datetime(1601, 1, 1))

    if sort is None:
        sort = 'displayName'
    all_ad_users.sort(key=lambda x: get_value(x, sort))

    for entry in all_ad_users:
        if entry.company == company:
            selection.append(entry)

    context = {
        'company': company,
        'zero_lock_datetime': zero_lock_datetime,
    }

    context.update(get_actionlog())

    db = Entry.objects.all()
    for d in db:
        print(d.sn.value)

    if len(selection) == 0:
        context['entries'] = all_ad_users
    else:
        context['entries'] = selection

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

            clear_dict(fields)

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
            return render(request, 'phonebook/create_ad_user.html',
                          {
                              'result': result['description'],
                              'result_send_mail': result_send_mail,
                              'account_name': account_name,
                              'form': form,
                          })
    else:
        form = CreateForm()

    return render(request, 'phonebook/create_ad_user.html', {'form': form})


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
