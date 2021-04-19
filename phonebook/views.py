import ldap3
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ldap3 import Connection, SUBTREE, ALL_ATTRIBUTES, MODIFY_REPLACE
import os

from ldap3.core.exceptions import LDAPCursorAttributeError

from phonebook_django.settings import CACHE_TTL

AD_SEARCH_TREE = 'dc=gk,dc=local'
AD_SERVER = os.environ.get('AD_SERVER')
AD_USER = os.environ.get('AD_USER')
AD_PASSWORD = os.environ.get('AD_PASSWORD')


def server_request():
    conn = Connection(server=AD_SERVER, user=AD_USER, password=AD_PASSWORD)
    conn.bind()

    # (!(UserAccountControl:1.2.840.113556.1.4.803 := 2)) активные учетные записи
    conn.search(AD_SEARCH_TREE,
                '(&(objectCategory=Person)(&(company=*)))',
                SUBTREE,
                attributes=[ALL_ATTRIBUTES]
                )
    return conn.entries


class Employee:
    """Запись из Active Directory (Person)"""

    def __init__(self,
                 account_name, display_name, company, title, department,
                 office, phone, mobile, email, last_logon, user_control, bad_pwd_count, create_user, lockout_time):
        self._account_name = account_name
        self._display_name = display_name
        self._company = company
        self._title = title
        self._department = department
        self._office = office
        self._phone = phone
        self._mobile = mobile
        self._email = email
        self._last_logon = last_logon
        self._user_control = user_control
        self._bad_pwd_count = bad_pwd_count
        self._create_user = create_user
        self._lockout_time = lockout_time

    def __str__(self):
        return self._account_name

    @property
    def account_name(self):
        return self._account_name

    @property
    def display_name(self):
        return self._display_name

    @property
    def company(self):
        return self._company

    @property
    def title(self):
        return self._title

    @property
    def department(self):
        return self._department

    @property
    def office(self):
        return self._office

    @property
    def phone(self):
        return self._phone

    @property
    def mobile(self):
        return self._mobile

    @property
    def email(self):
        return self._email

    @property
    def last_logon(self):
        return self._last_logon

    @property
    def user_control(self):
        return self._user_control

    @property
    def bad_pwd_count(self):
        return self._bad_pwd_count

    @property
    def create_user(self):
        return self._create_user

    @property
    def lockout_time(self):
        return self._lockout_time


class EmployeeList:
    """Список объектов класса Employee"""

    def __init__(self):
        self.employee_list = []

    @property
    def register(self):
        return self.employee_list

    @register.setter
    def register(self, value):
        self.employee_list.append(value)

    def company(self, company):
        filter_company = []
        if company == 'all':
            return self.employee_list
        else:
            for entry in self.employee_list:
                if entry.company == company:
                    filter_company.append(entry)
            return filter_company

    def sort(self, sort_value):
        try:
            return self.employee_list.sort(key=lambda x: getattr(x, sort_value))
        except AttributeError:
            print(f'Object has no attribute {sort_value}')


def transfer(entries):
    employers = EmployeeList()
    for entry in entries:
        employers.register = (Employee(
            account_name=str(entry.sAMAccountName),
            display_name=str(entry.displayName),
            company=str(entry.company),
            title=str(entry.title),
            department=str(entry.department),
            office=str(entry.physicalDeliveryOfficeName),
            phone=str(entry.telephoneNumber),
            mobile=str(entry.mobile),
            email=str(entry.mail),
            last_logon=str(entry.lastLogon),
            user_control=str(entry.userAccountControl),
            bad_pwd_count=str(entry.badPwdCount),
            create_user=str(entry.createTimeStamp),
            lockout_time=str(entry.lockoutTime),
        ))
    return employers


# @cache_page(CACHE_TTL)
def index2(request, company='all'):
    employers = transfer(server_request())
    if 'sort' in request.GET:
        sort_value = request.GET.get('sort')
        employers.sort(sort_value)
    else:
        sort_value = 'display_name'
        employers.sort(sort_value)

    context = {
        'entries': employers.company(company=company),
    }
    return render(request, 'phonebook/index.html', context)


@login_required
def user_control(request, company='all'):
    employers = transfer(server_request())
    if 'sort' in request.GET:
        sort_value = request.GET.get('sort')
        employers.sort(sort_value)
    else:
        sort_value = 'display_name'
        employers.sort(sort_value)

    context = {
        'entries': employers.company(company=company),
    }
    return render(request, 'phonebook/users.html', context)


def index(request):
    selection = []
    all_users = server_request()
    sort = request.GET.get('sort')
    company = request.GET.get('company')

    if sort is None:
        sort = 'displayName'

    try:
        all_users.sort(key=lambda x: x.displayName.value)
        # all_users.sort(key=lambda x: getattr(x, sort, ''))
    except LDAPCursorAttributeError:
        print(f'Attribute {sort} not found')

    for entry in all_users:
        if entry.company.value == company:
            selection.append(entry)

    if len(selection) == 0:
        context = {'entries': all_users, 'company': company}
    else:
        context = {'entries': selection, 'company': company}

    return render(request, 'phonebook/index.html', context)


def users(request):
    sort = request.GET.get('sort')
    company = request.GET.get('company')
    selection = []
    all_users = server_request()

    try:
        all_users.sort(key=lambda x: x.displayName.value)
    except LDAPCursorAttributeError:
        print(f'Attribute {sort} not found')

    for entry in all_users:
        # if hasattr(entry, 'lockoutTime') is False:
        if entry.userAccountControl == 514 or 66050:
            selection.append(entry)

    context = {
        'entries': selection,
        'all_users': all_users
    }
    return render(request, 'phonebook/users.html', context)


def state(request):
    conn = Connection(AD_SERVER, AD_USER, AD_PASSWORD)
    conn.bind()

    user = request.GET.get('user')
    state = request.GET.get('state')
    if state == 'disable':
        state = 514
    print(user)

    conn.modify(user,
                {'userAccountControl': [(MODIFY_REPLACE, [state])]})
    print(conn.result)
    conn.unbind()

    return HttpResponseRedirect(reverse('phonebook:users'))
