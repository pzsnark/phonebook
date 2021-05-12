from ldap3.core.exceptions import LDAPCursorAttributeError
from .models import VisitLog
import socket


# получаем значение из объекта
def get_value(obj, field):
    try:
        result = getattr(obj, field).value
    except LDAPCursorAttributeError:
        result = ''
    return result


# очищаем словарь от ключей с пустыми значениями
def clear_dict(dictionary):
    dict_copy = dictionary.copy()
    for key in dict_copy:
        if dictionary.get(key) == '':
            dictionary.pop(key)
    return dictionary


# записываем данные посещения
def visit_log(request):
    ipaddress = request.META.get('REMOTE_ADDR')
    hostname = (socket.gethostbyaddr(ipaddress))[0]
    print(hostname)
    http_referer = request.META.get('HTTP_REFERER')
    visit = VisitLog(ipaddress=ipaddress, hostname=hostname, http_referer=http_referer)
    visit.save()


def get_visit_log():
    all_records = VisitLog.objects.all().order_by('date')
    unique_records = VisitLog.objects.order_by().values('ipaddress').distinct()
    visit_counts = {'all_records': all_records, 'unique_records': unique_records}
    return visit_counts
