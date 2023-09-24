from django.urls import path
from . import views


urlpatterns =[
    path('', views.int_entrada, name='int_entrada'),
    path('salir/', views.salir, name="salir"),
    path('agregarRegistro/', views.registrarvehiculo, name='agregarRegistro'),
     path('contador/', views.obtener_contador, name='contador'),
    
]