from django.utils import timezone
from django.db import models


class ActionLog(models.Model):
    ipaddress = models.GenericIPAddressField(protocol='ipv4', db_index=True)
    username = models.CharField(max_length=255, null=True)
    hostname = models.CharField(max_length=255, null=True)
    path = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.ipaddress)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
