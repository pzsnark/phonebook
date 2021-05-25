from django.urls import path

from . import views

app_name = "phonebook"

urlpatterns = [
    path('', views.index, name='index'),
    path('status/', views.status, name='status'),
    path('create/', views.create_ad_user, name='create'),
]
