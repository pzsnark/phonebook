from django.urls import path

from . import views

app_name = "phonebook"

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:company>', views.filter_by_company, name='company'),
    path('<str:company>/', views.index, name='index'),
]
