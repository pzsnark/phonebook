from django.urls import path

from . import views

app_name = "phonebook"

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:company>', views.quest, name='company'),
    path('book/book.xml', views.book_xml, name='book_xml'),
]
