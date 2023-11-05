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
from random import randrange
import random
from django.db.models import F
from datetime import datetime



# Create your views here.
##@login_required
def int_entrada(request):
    totaldisponibles = obtener_total_disponibles()
    totaldisponiblesmotos = obtener_total_disponibles2()
    totaldisponiblesmicros = obtener_total_disponibles3()
    totaldisponblestodos=obtener_total_disponibles4()
    return render(request, 'interfaz_entrada.html', {
        'totaldisponibles': totaldisponibles[0],
        'totaldisponiblesmotos': totaldisponiblesmotos[0],
        'totaldisponiblesmicros': totaldisponiblesmicros[0],
        'totaldisponblestodos': totaldisponblestodos[0]

    })

def salir(request):
    logout(request)
    return redirect('/')
def obtener_contador(request):
    totaldisponibles = obtener_total_disponibles()
    totaldisponiblesmotos = obtener_total_disponibles2()
    totaldisponiblesmicros = obtener_total_disponibles3()
    totaldisponblestodos=obtener_total_disponibles4()
    return JsonResponse({
        'totaldisponibles': totaldisponibles[0],
        'totaldisponiblesmotos': totaldisponiblesmotos[0],
        'totaldisponiblesmicros': totaldisponiblesmicros[0],
        'totaldisponblestodos': totaldisponblestodos[0]
    })

"""--------Apartado interfaces-----"""

def int_salida(request):
    registros=RegistroVehiculos.objects.filter(Estado='A')
    listado={'registros':registros}
    return render(request, 'interfaz_salida.html',listado)
def int_historial(request):
    return render(request, 'historia.html')
def int_configuration(request):
    return render(request, 'configuration.html')
def int_perfil(request):
    return render(request, 'perfil.html')



def registrarvehiculo(request):
    if request.method == 'POST':
        Hora_de_salidadefecto = time(0, 0, 0).strftime('%H:%M:%S')
        hora_actual = datetime.now().time().strftime('%H:%M:%S')
        Matricula = request.POST['Matricula']
        Tipo_de_vehiculo = request.POST['tipoVehiculo']
        Usuario = request.POST['rol']
        Fecha = request.POST['fechaActual']
        Hora_de_entrada = hora_actual
        Estado = 'A'
        Id_tabla_historial_value=request.POST['Id_tabla_historial']

        
                    
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
        try:
            with transaction.atomic():
                parqueo_disponible = ParqueoDisponible.objects.get(idParqueoDisponibel=Id_tabla_historial_value)
                parqueo_disponible.TotalParqueoDisponible -= 1
                parqueo_disponible.save()
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la actualización de parqueos disponibles
            return HttpResponse(f"Error al actualizar parqueos disponibles: {str(e)}")
        
            

        return redirect('int_entrada')
def actualizar_registro(request, idregistrovehiculos):
    
    hora_actual = datetime.now().time()  # Obtén la hora actual
    Hora_de_salida=hora_actual
    try:
        with transaction.atomic():
            # Actualiza el registro en la tabla de registro de vehículos
            with connection.cursor() as cursor:
                cursor.execute("UPDATE interfaz_Entrada_registrovehiculos SET estado='I', Hora_de_salida=%s WHERE idregistrovehiculos=%s",
                               [Hora_de_salida, idregistrovehiculos])

            # Incrementa la disponibilidad de parqueo
            parqueo_disponible = ParqueoDisponible.objects.first()
            parqueo_disponible.TotalParqueoDisponible += 1
            parqueo_disponible.save()

            return redirect('int_salida')
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la actualización
        return HttpResponse(f"Error al actualizar el registro: {str(e)}")
def actualizar_registros(request, idregistrovehiculos):
    hora_actual = datetime.now().time()  # Obtén la hora actual
    hora_actual_formateada = hora_actual.strftime("%H:%M")
    try:
        with transaction.atomic():
            # Obtén el registro de vehículos por su ID y actualízalo
            registro_vehiculo = RegistroVehiculos.objects.get(pk=idregistrovehiculos)
            Id_tabla_historial = registro_vehiculo.Id_tabla_historial_id
            registro_vehiculo.Estado = 'I'
            registro_vehiculo.Hora_de_salida = hora_actual_formateada
            registro_vehiculo.save()

            # Incrementa la disponibilidad de parqueo
            parqueo_disponible = ParqueoDisponible.objects.get(idParqueoDisponibel=Id_tabla_historial)
            parqueo_disponible.TotalParqueoDisponible += 1
            parqueo_disponible.save()

            return redirect('int_salida')
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la actualización
        return HttpResponse(f"Error al actualizar el registro: {str(e)}")
    


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
        cursor.execute("select TotalParqueoDisponible from interfaz_Entrada_parqueodisponible where idParqueoDisponibel=1")           
    totaldisponibles = cursor.fetchone()  
    return totaldisponibles
def obtener_total_disponibles2():
    with connection.cursor() as cursor:
        cursor.execute("select TotalParqueoDisponible from interfaz_Entrada_parqueodisponible where idParqueoDisponibel=2")           
    totaldisponibles = cursor.fetchone()  
    return totaldisponibles
def obtener_total_disponibles3():
    with connection.cursor() as cursor:
        cursor.execute("select TotalParqueoDisponible from interfaz_Entrada_parqueodisponible where idParqueoDisponibel=3")           
    totaldisponibles = cursor.fetchone()  
    return totaldisponibles
def obtener_total_disponibles4():
    with connection.cursor() as cursor:
        cursor.execute("select sum(TotalParqueoDisponible) from interfaz_Entrada_parqueodisponible")           
    totaldisponibles = cursor.fetchone()  
    return totaldisponibles



def registros_de_parqueosuso():
    with connection.cursor() as cursor:
        cursor.execute("select Tipo_de_vehiculo,fecha,Hora_de_entrada,Usuario,Estado from interfaz_Entrada_registrovehiculos where Estado='A' ")
    registrosparqueos = cursor.fetchall()
    return registrosparqueos

def salida_vehiculo(Hora_de_salida,idregistrovehiculos):
    with connection.cursor() as cursor:
        cursor.execute("update interfaz_Entrada_registrovehiculos set estado='I',Hora_de_salida=%s where idregistrovehiculos=%s",
                       (Hora_de_salida,idregistrovehiculos))
    connection.commit()
    connection.close()
