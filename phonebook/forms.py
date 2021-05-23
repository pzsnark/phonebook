from django import forms
from .models import Entry
from .utils import company_list


class Select(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        if option.get('value') == "ABZ":
            option['attrs']['disabled'] = 'disabled'

        return option


class CreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['company'].choices = company_list()

    last_name = forms.CharField(label='Фамилия', max_length=100)
    first_name = forms.CharField(label='Имя', max_length=100)
    middle_name = forms.CharField(label='Отчество', max_length=100)
    title = forms.CharField(label='Должность', max_length=100, required=None)
    department = forms.CharField(label='Отдел', max_length=100, required=None)
    location = forms.CharField(label='Местоположение', max_length=100, required=None)
    email = forms.EmailField(label='Email', max_length=100, required=None)
    phone = forms.CharField(label='Внутренний телефон', max_length=4, required=None)
    mobile = forms.CharField(label='Сотовый телефон', max_length=12, required=None)
    company = forms.ChoiceField(choices=company_list(), label='Организация')


class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['company'].choices = company_list()

    model = Entry

    company = forms.ChoiceField(choices=company_list(), label='Организация')
    displayName = forms.CharField(label='ФИО', max_length=100, required=None, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        self.cleaned_data['displayName'] = f'{self.cleaned_data["sn"]} {self.cleaned_data["givenName"]} {self.cleaned_data["middle_name"]}'
        return cleaned_data
