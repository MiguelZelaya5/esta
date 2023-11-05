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

@login_required
def inicio(request):
    return render(request, 'interfaz_entrada.html')
@login_required
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
@login_required
def salir(request):
    logout(request)
    return redirect('/')
@login_required
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
@login_required
def int_salida(request):
    registros = RegistroVehiculos.objects.filter(Estado='A')
    registros_data = []

    for registro in registros:
        tiempo_transcurrido = calcularTiempoTranscurrido(registro.Hora_de_entrada)
        registros_data.append({
            'idregistrovehiculos': registro.idregistrovehiculos,
            'Matricula': registro.Matricula,
            'Tipo_de_vehiculo':registro.Tipo_de_vehiculo,
            'fecha':registro.fecha,
            'Hora_de_entrada':registro.Hora_de_entrada,
            'TiempoTranscurrido': tiempo_transcurrido,
            'Usuario':registro.Usuario,
            'Estado':registro.Estado
        })

    # Renderiza la plantilla HTML y pasa los datos a la misma
    return render(request, 'interfaz_salida.html', {'registros': registros_data})
@login_required
def int_historial(request):
    return render(request, 'historia.html')
@login_required
def int_configuration(request):
    return render(request, 'configuration.html')
@login_required
def int_perfil(request):
    return render(request, 'perfil.html')


def calcularTiempoTranscurrido(hora_entrada):
    # Obtiene la hora actual
    ahora = datetime.now().time()

    # Calcula la diferencia de tiempo
    horas = ahora.hour - hora_entrada.hour
    minutos = ahora.minute - hora_entrada.minute
    segundos = ahora.second - hora_entrada.second

    # Asegura que los valores estén en el rango correcto
    if segundos < 0:
        segundos += 60
        minutos -= 1
    if minutos < 0:
        minutos += 60
        horas -= 1
    if horas < 0:
        horas += 24  # 24 horas en un día

    # Devuelve el tiempo transcurrido en formato "HH:MM:SS"
    tiempo_transcurrido = f'{horas:02d}:{minutos:02d}:{segundos:02d}'
    return tiempo_transcurrido


def obtener_tiempo(request):
    registros = RegistroVehiculos.objects.filter(Estado='A')
    tiempo_transcurrido = {}

    for registro in registros:
        tiempo = calcularTiempoTranscurrido(registro.Hora_de_entrada)
        tiempo_transcurrido[registro.idregistrovehiculos] = tiempo

    return JsonResponse(tiempo_transcurrido)

@login_required
def eliminarRegistro(request, idregistrovehiculos):
    registro_vehiculo = RegistroVehiculos.objects.get(pk=idregistrovehiculos)
    Id_tabla_historial = registro_vehiculo.Id_tabla_historial_id  # Acceder directamente al ID de la clave externa
    parqueo_disponible = ParqueoDisponible.objects.get(idParqueoDisponibel=Id_tabla_historial)
    parqueo_disponible.TotalParqueoDisponible += 1
    parqueo_disponible.save()
    registro_vehiculo.delete()

    return redirect('int_salida')


@login_required
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
    
@login_required
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

@login_required
def obtener_datos_para_grafico(request, anio=None):
    with connection.cursor() as cursor:
        if anio:
            cursor.execute("""
                SELECT MONTH(fecha) AS Mes, COALESCE(COUNT(*), 0) AS Total
                FROM interfaz_Entrada_registrovehiculos
                WHERE YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
            """, [anio])
        else:
            cursor.execute("""
                SELECT MONTH(fecha) AS Mes, COALESCE(COUNT(*), 0) AS Total
                FROM interfaz_Entrada_registrovehiculos
                GROUP BY MONTH(fecha)
            """)

        data = cursor.fetchall()

    # Ordena los datos por mes antes de enviarlos como respuesta JSON
    resultados = sorted([{'Mes': row[0], 'Total': row[1]} for row in data], key=lambda x: x['Mes'])

    return JsonResponse({'resultados': resultados})

@login_required
def obtener_anios(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT YEAR(fecha) AS Anio 
            FROM interfaz_Entrada_registrovehiculos
            ORDER BY Anio DESC
        """)
        anios = [row[0] for row in cursor.fetchall()]

    return JsonResponse({'anios': anios})

@login_required
def get_chart(_request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MONTH(fecha) AS Mes, COUNT(*) AS Total
            FROM interfaz_Entrada_registrovehiculos 
            GROUP BY MONTH(fecha)
        """)
        data = cursor.fetchall()

    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    random_color = random.choice(['blue', 'orange', 'red', 'green', 'purple', 'brown', 'pink'])

    serie = []
    xAxis_data = []

    for mes in range(1, 13):
        # Comprobamos si hay datos para el mes actual
        mes_existente = any(row[0] == mes for row in data)
        if mes_existente:
            total_mes = next((row[1] for row in data if row[0] == mes), 0)
        else:
            total_mes = 0

        serie.append(total_mes)
        xAxis_data.append(meses[mes - 1])

    chart = {
        'tooltip': {
            'show': True,
            'trigger': 'axis',
            'triggerOn': 'mousemove|click'
        },
        'xAxis': [
            {
                'type': 'category',
                'data': xAxis_data
            }
        ],
        'yAxis': [
            {
                'type': 'value'
            }
        ],
        'series': [
            {
                'data': serie,
                'type': 'line',
                'itemStyle': {
                    'color': random_color
                },
                'lineStyle': {
                    'color': random_color
                }
            }
        ]
    }

    return JsonResponse(chart)