from django.utils.deprecation import MiddlewareMixin
from .models import ActionLog
import socket


class ActionLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.META)
        ipaddress = request.META.get('REMOTE_ADDR')
        user = request.user
        try:
            hostname = (socket.gethostbyaddr(ipaddress))[0]
        except socket.herror:
            return None, None, None
        http_referer = request.META.get('HTTP_REFERER')
        visit = ActionLog(ipaddress=ipaddress, hostname=hostname, http_referer=http_referer, user=user)
        visit.save()
