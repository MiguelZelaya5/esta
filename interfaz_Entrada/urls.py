from django.urls import path
from . import views


urlpatterns =[
    path('', views.int_entrada),
]