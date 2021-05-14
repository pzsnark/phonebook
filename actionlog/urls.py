from django.urls import path

from . import views

app_name = "actionlog"

urlpatterns = [
    path('', views.actionlog_view, name='actionlog_view')
]
