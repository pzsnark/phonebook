from django.urls import path

from . import views

app_name = "phonebook"

urlpatterns = [
    path('', views.index, {'company': 'all'}, name='index'),
    path('<str:company>/', views.index, name='index'),
    path('<str:company>/users/', views.user_control, {'company': 'all'}, name='user_control'),
]
