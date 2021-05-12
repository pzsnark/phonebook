import datetime
from django.utils import timezone
from django.db import models


class VisitLog(models.Model):
    ipaddress = models.GenericIPAddressField(protocol='ipv4')
    hostname = models.CharField(max_length=255, null=True)
    http_referer = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.ipaddress)
