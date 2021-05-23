from django.utils.deprecation import MiddlewareMixin


# class VisitLogMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         ipaddress = request.META.get('REMOTE_ADDR')
#         hostname = request.META.get('REMOTE_HOSbT')
#         username = request.META.get('USERNAME')
#         visit = VisitLog(ipaddress=ipaddress, hostname=hostname, username=username)
#         logger.debug(visit.ipaddress, visit.hostname, visit.username)
#         visit.save()
