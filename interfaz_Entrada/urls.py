from django.urls import path
from . import views


urlpatterns =[
    path('', views.inicio, name='inicio'),
    path('int_entrada', views.int_entrada, name='int_entrada'),
    path('int_busqueda', views.int_busqueda, name='int_busqueda'),
    path('int_salida', views.int_salida, name='int_salida'),
    path('historial', views.int_historial, name='historial'),
    path('configura', views.int_configuration, name='configura'),
    path('perfil', views.int_perfil, name='perfil'),
    path('salir/', views.salir, name="salir"),
    path('agregarRegistro/', views.registrarvehiculo, name='agregarRegistro'),
    path('contador/', views.obtener_contador, name='contador'),
    path('calculartime/', views.obtener_tiempo, name='calculartime'),
    path('eliminarregistros/<idregistrovehiculos>', views.eliminarRegistro),
    path('registrospormatricula/eliminarregistros2/<int:idregistrovehiculos>/<matricula>', views.eliminarRegistro2, name='eliminarregistros2'),
    path('registrospormatricula/<matricula>', views.registros_por_matricula),
    path('actualizarregistros/<idregistrovehiculos>', views.actualizar_registros),

    path('int_salidaAc/<InEid>', views.actualizar_registros),
    path('get_chart/', views.get_chart, name='get_chart'),
    path('obtener-anios/', views.obtener_anios, name='obtener_anios'),
    path('obtener-datos-para-grafico/<int:anio>/', views.obtener_datos_para_grafico, name='obtener_datos_para_grafico'),
    path('redirigir-a-admin/', views.redirigir_a_admin, name='redirigir_a_admin'),
    
    
    
]