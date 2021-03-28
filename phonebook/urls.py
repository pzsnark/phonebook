from django.urls import path

from . import views

app_name = "phonebook"

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:company>', views.filter_by_company, name='company'),
    path('test/<str:company>', views.test2, name='test'),
]
