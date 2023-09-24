from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.db import models
from django.db import connection
from interfaz_Entrada.models import RegistroVehiculos,HistorialYEstadisticas

# Create your views here.
##@login_required
def int_entrada(request):
    return render(request, 'interfaz_entrada.html')

def salir(request):
    logout(request)
    return redirect('/')


def registrarvehiculo(request):
    if request.method=='POST':
        Hora_de_salidadefecto=time(0,0,0)
        hora_actual = datetime.now().time()
        '''hora_ajustada = hora_actual - timedelta(hours=2)'''
        Matricula=request.POST['Matricula']
        Tipo_de_vehiculo=request.POST['tipoVehiculo']
        Usuario=request.POST['rol']
        Fecha=request.POST['fechaActual']
        Hora_de_entrada=hora_actual
        Estado='A'
        Id_tabla_historial_value=request.POST['Id_tabla_historial']

        try:
            # Busca un objeto HistorialYEstadisticas por su id
            Id_tabla_historial_obj = HistorialYEstadisticas.objects.get(pk=Id_tabla_historial_value)
        except HistorialYEstadisticas.DoesNotExist:
            # Maneja el caso en el que el objeto no existe
            Id_tabla_historial_obj = None
        RegistroVehiculos(Tipo_de_vehiculo=Tipo_de_vehiculo,Matricula=Matricula,Fecha=Fecha,Hora_de_entrada=Hora_de_entrada,Hora_de_salida=Hora_de_salidadefecto,Usuario=Usuario,
                      Estado=Estado,Id_tabla_historial=Id_tabla_historial_obj).save()
        return render(request,'interfaz_entrada.html')
    else:
        return render(request,'interfaz_entrada.html')
    

"""
def registrarvehiculo(request):
    if request.method == 'POST':
        Hora_de_salidadefecto = time(0, 0, 0)
        hora_actual = datetime.now().time()
        hora_ajustada = hora_actual - timedelta(hours=2)
        Matricula = request.POST['matricula']
        Tipo_de_vehiculo = request.POST['tipoVehiculo']
        Usuario = request.POST['rol']
        Fecha = request.POST['fechaActual']
        Hora_de_entrada = hora_ajustada
        Estado = 'A'
        Id_tabla_historial = request.POST['Id_tabla_historial']
        
        # Llama al método insertar_vehiculos para insertar los datos en la base de datos
        insertar_interfaz_Entrada_registrovehiculos(
            Tipo_de_vehiculo=Tipo_de_vehiculo,
            Matricula=Matricula,
            Fecha=Fecha,
            Hora_de_entrada=Hora_de_entrada,
            Hora_de_salida=Hora_de_salidadefecto,
            Usuario=Usuario,
            Estado=Estado,
            Id_tabla_historial=Id_tabla_historial
        )

        return render(request, 'interfaz_entrada.html')
    else:
        return render(request, 'interfaz_entrada.html')

    
def insertar_interfaz_Entrada_registrovehiculos(Tipo_de_vehiculo,Matricula,Fecha,Hora_de_entrada,Hora_de_salida,Usuario,
                      Estado,Id_tabla_historial):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO interfaz_Entrada_registrovehiculos(Tipo_de_vehiculo,Matricula,Fecha,Hora_de_entrada,Hora_de_salida,Usuario,Estado,Id_tabla_historial) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)",
                       (Tipo_de_vehiculo,Matricula,Fecha,Hora_de_entrada,Hora_de_salida,Usuario,
                      Estado,Id_tabla_historial))
    connection.commit()
    connection.close()
"""


       
