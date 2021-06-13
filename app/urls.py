from django.urls import path

from .views import detail

urlpatterns = [path('',detail,name='detail')]