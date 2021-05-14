from django.utils import timezone
from django.db import models


class ActionLog(models.Model):
    ipaddress = models.GenericIPAddressField(protocol='ipv4')
    user = models.CharField(max_length=255, null=True)
    hostname = models.CharField(max_length=255, null=True)
    http_referer = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.ipaddress)
