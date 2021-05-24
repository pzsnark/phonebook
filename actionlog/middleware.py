from django.utils.deprecation import MiddlewareMixin
from .models import ActionLog
from .conf import EXCLUDE_IPADDR
import socket


class ActionLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ipaddress = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = 'Anon'

        try:
            hostname = (socket.gethostbyaddr(ipaddress))[0]
        except socket.herror:
            hostname = ipaddress

        http_referer = request.META.get('HTTP_REFERER')
        visit = ActionLog(ipaddress=ipaddress, hostname=hostname, http_referer=http_referer, user=user)

        if visit.ipaddress not in EXCLUDE_IPADDR:
            visit.save()
