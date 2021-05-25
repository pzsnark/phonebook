from django.utils.deprecation import MiddlewareMixin
from .models import ActionLog
from .conf import EXCLUDE_IPADDR
import socket


class ActionLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ipaddress = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = ''

        try:
            hostname = (socket.gethostbyaddr(ipaddress))[0]
        except socket.herror:
            hostname = ipaddress

        path = request.get_full_path()
        visit = ActionLog(ipaddress=ipaddress, hostname=hostname, path=path, username=username)

        if visit.ipaddress not in EXCLUDE_IPADDR:
            visit.save()
