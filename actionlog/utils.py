from .models import ActionLog
import socket


def get_actionlog():
    all_records = ActionLog.objects.all().order_by('-date')
    unique_records = ActionLog.objects.order_by().values('ipaddress').distinct()
    visit_counts = {'all_records': all_records, 'unique_records': unique_records}
    return visit_counts
