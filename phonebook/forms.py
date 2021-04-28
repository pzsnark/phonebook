from django import forms
# from django.contrib.auth import forms
import unicodedata


class Select(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        if option.get('value') == "ABZ":
            option['attrs']['disabled'] = 'disabled'

        return option


class UsernameFields:
    def to_python(self, value):
        value = value.lower()
        return unicodedata.normalize('NFKC', super().to_python(value))


class CreateADUserForm(forms.Form):

    COMPANY_CHOICES = [
        ('', 'Выберите организацию'),
        ('ABZ', 'АБЗ №1'),
        ('AVS', 'Автоволгастрой'),
        ('SMT', 'СМУ Тольятти'),
        ('SMS', 'СМУ Самара'),
        ('ODS', 'Облдорстрой'),
        ('PRS', 'Перспектива'),
        ('PNL', 'ПНЛ'),
        ('AVN', 'Авангард'),
    ]

    last_name = forms.CharField(label='Фамилия', max_length=100)
    first_name = forms.CharField(label='Имя', max_length=100)
    middle_name = forms.CharField(label='Отчество', max_length=100)
    title = forms.CharField(label='Должность', max_length=100, required=None)
    department = forms.CharField(label='Отдел', max_length=100, required=None)
    location = forms.CharField(label='Местоположение', max_length=100, required=None)
    email = forms.EmailField(label='Email', max_length=100, required=None)
    phone = forms.CharField(label='Внутренний телефон', max_length=100, required=None)
    mobile = forms.CharField(label='Сотовый телефон', max_length=12, required=None)
    company = forms.ChoiceField(choices=COMPANY_CHOICES, label='Организация')
