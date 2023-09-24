from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime, timedelta, time
from django.db import models
from django.db import connection
from interfaz_Entrada.models import RegistroVehiculos,HistorialYEstadisticas,ParqueoDisponible
from django.db import transaction
from django.http import JsonResponse



# Create your views here.
##@login_required
def int_entrada(request):
    totaldisponibles = obtener_total_disponibles()
    return render(request, 'interfaz_entrada.html')

def salir(request):
    logout(request)
    return redirect('/')


def registrarvehiculo(request):
    if request.method == 'POST':
        Hora_de_salidadefecto = time(0, 0, 0)
        hora_actual = datetime.now().time()
        Matricula = request.POST['Matricula']
        Tipo_de_vehiculo = request.POST['tipoVehiculo']
        Usuario = request.POST['rol']
        Fecha = request.POST['fechaActual']
        Hora_de_entrada = hora_actual
        Estado = 'A'
        Id_tabla_historial_value=request.POST['Id_tabla_historial']

        parqueo_disponible = ParqueoDisponible.objects.first()
        if parqueo_disponible.TotalParqueoDisponible > 0:
            try:
                with transaction.atomic():
                    # Actualizar parqueos disponibles
                    parqueo_disponible.TotalParqueoDisponible -= 1
                    parqueo_disponible.save()
                    
                    # Llama al método insertar_vehiculos para insertar los datos en la base de datos
                    insertar_interfaz_Entrada_registrovehiculos(
                        Tipo_de_vehiculo=Tipo_de_vehiculo,
                        Matricula=Matricula,
                        fecha=Fecha,
                        Hora_de_entrada=Hora_de_entrada,
                        Hora_de_salida=Hora_de_salidadefecto,
                        Usuario=Usuario,
                        Estado=Estado,
                        Id_tabla_historial=Id_tabla_historial_value
                    )
            except Exception as e:
                # Manejar cualquier error que pueda ocurrir durante la actualización de parqueos disponibles
                return HttpResponse(f"Error al actualizar parqueos disponibles: {str(e)}")

        return render(request, 'interfaz_entrada.html')


def insertar_interfaz_Entrada_registrovehiculos(Tipo_de_vehiculo,Matricula,fecha,Hora_de_entrada,Hora_de_salida,Usuario,
                        Estado,Id_tabla_historial):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO interfaz_Entrada_registrovehiculos(Tipo_de_vehiculo,Matricula,fecha,Hora_de_entrada,Hora_de_salida,Usuario,Estado,Id_tabla_historial) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)",
                        (Tipo_de_vehiculo,Matricula,fecha,Hora_de_entrada,Hora_de_salida,Usuario,
                        Estado,Id_tabla_historial))
        connection.commit()
        connection.close()

def obtener_total_disponibles():
    with connection.cursor() as cursor:
        cursor.execute("select TotalParqueoDisponible from interfaz_Entrada_parqueodisponible")           
    totaldisponibles = cursor.fetchone()  
    return totaldisponibles




       
