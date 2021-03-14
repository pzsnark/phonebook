from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abz', views.abz, name='abz'),
    path('query', views.query, name='query'),
]
