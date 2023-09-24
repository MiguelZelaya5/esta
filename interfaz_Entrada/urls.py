from django.urls import path
from . import views


urlpatterns =[
    path('', views.int_entrada),
    path('salir/', views.salir, name="salir"),
    path('agregarRegistro/', views.registrarvehiculo, name='agregarRegistro'),
    
]