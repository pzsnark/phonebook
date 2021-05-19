import json

from django.db import models


class Company(models.Model):
    name = models.CharField('Компания', max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Entry(models.Model):
    sn = models.CharField('Фамилия', max_length=255)
    givenName = models.CharField('Имя', max_length=255)
    middle_name = models.CharField('Отчество', max_length=255)
    title = models.CharField('Должность', max_length=255, null=True, blank=True)
    department = models.CharField('Отдел', max_length=255, null=True, blank=True)
    physicalDeliveryOfficeName = models.CharField('Местонахождения', max_length=255, null=True, blank=True)
    mail = models.CharField('Почта', max_length=255, null=True, blank=True)
    telephoneNumber = models.CharField('Внутренний', max_length=4, null=True, blank=True)
    mobile = models.CharField('Мобильный', max_length=15, null=True, blank=True)
    company = models.ForeignKey(Company, related_name='company', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.sn} {self.givenName}'

    @property
    def displayname(self):
        return f'{self.sn} {self.givenName} {self.middle_name}'

    @classmethod
    def to_json(cls):
        return json.dumps(Entry.__dict__)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
