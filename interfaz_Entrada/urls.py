from django.urls import path
from . import views


urlpatterns =[
    path('int_entrada', views.int_entrada, name='int_entrada'),
    path('int_salida', views.int_salida, name='int_salida'),
    path('historial', views.int_historial, name='historial'),
    path('configura', views.int_configuration, name='configura'),
    path('perfil', views.int_perfil, name='perfil'),
    path('salir/', views.salir, name="salir"),
    path('agregarRegistro/', views.registrarvehiculo, name='agregarRegistro'),
    path('contador/', views.obtener_contador, name='contador'),
    
]