import json

from django.db import models
from django.core import serializers


class Company(models.Model):
    name = models.CharField('Компания', max_length=50)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Entry(models.Model):
    sn = models.CharField('Фамилия', max_length=255)
    givenName = models.CharField('Имя', max_length=255)
    middle_name = models.CharField('Отчество', max_length=255)
    displayName = models.CharField('ФИО', max_length=255, default='', null=True, blank=True)
    title = models.CharField('Должность', max_length=255, null=True, blank=True)
    department = models.CharField('Отдел', max_length=255, null=True, blank=True)
    physicalDeliveryOfficeName = models.CharField('Местоположение', max_length=255, null=True, blank=True)
    mail = models.CharField('Почта', max_length=255, null=True, blank=True)
    telephoneNumber = models.CharField('Внутренний', max_length=4, null=True, blank=True)
    mobile = models.CharField('Мобильный', max_length=15, null=True, blank=True)
    company = models.CharField('Компания', max_length=255, default=None)

    def __str__(self):
        return f'{self.sn} {self.givenName}'

    # @property
    # def displayName(self):
    #     return f'{self.sn} {self.givenName} {self.middle_name}'

    @classmethod
    def model_to_json(cls):
        all_entries = list(Entry.objects.values())
        return all_entries

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
