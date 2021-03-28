import ldap3
from django.shortcuts import render
from ldap3 import Connection, SUBTREE

AD_SERVER = 'dc2.gk.local'
AD_USER = 'ldap-bot@gk.local'
AD_PASSWORD = '12345678'
AD_SEARCH_TREE = 'dc=gk,dc=local'


def server_request():
    server = ldap3.Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)  # вынести реквизиты в окружение ОС
    conn.bind()

    conn.search(AD_SEARCH_TREE,
                '(&(objectCategory=Person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(&(company=*)))',
                SUBTREE,
                attributes=['department', 'sAMAccountName', 'displayName', 'physicalDeliveryOfficeName',
                            'telephoneNumber', 'mail', 'mobile', 'title', 'company', 'lastLogon']
                )
    return conn.entries


class Employee:
    """Запись из Active Directory (Person)"""

    def __init__(self,
                 account_name, display_name, company, title, department, office, phone, mobile, email, last_logon):
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

    def __str__(self):
        return self._account_name

    # def __eq__(self, other):
    #     return self.account_name == other.account_name

    # def __lt__(self, other):
    #     return self.display_name < other.display_name
    #
    # def __gt__(self, other):
    #     return self.display_name > other.display_name

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

    def is_sorting(self):
        return self.employee_list.sort(key=lambda x: x.company)


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
            last_logon=str(entry.lastLogon)
        ))
    return employers


def test2(request, company='all'):
    employers = transfer(server_request())
    employers.is_sorting()
    context = {
        'entries': employers.company(company=company),
    }
    return render(request, 'phonebook/test.html', context)


def index(request):
    entries = server_request()
    entries.sort()
    context = {
        'entries': entries
    }
    print(len(entries))
    return render(request, 'phonebook/index.html', context)


def filter_by_company(request, company):
    entries = []
    for entry in server_request():
        if entry.company == company:
            entries.append(entry)
    entries.sort()
    context = {
        'entries': entries
    }
    return render(request, 'phonebook/company.html', context)
