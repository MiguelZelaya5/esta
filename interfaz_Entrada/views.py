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






# Create your views here.
##@login_required
def int_entrada(request):
    totaldisponibles = obtener_total_disponibles()
    return render(request, 'interfaz_entrada.html', {'totaldisponibles': totaldisponibles[0]})

def salir(request):
    logout(request)
    return redirect('/')
def obtener_contador(request):
    totaldisponibles = obtener_total_disponibles()
    return JsonResponse({'totaldisponibles': totaldisponibles[0]})
"""--------Apartado interfaces-----"""

def int_salida(request):
    registros=RegistroVehiculos.objects.filter(Estado='A')
    registros_con_tiempo = []

    for registro in registros:
        tiempo_transcurrido = calcular_tiempo_transcurrido(registro.Hora_de_entrada, registro.Hora_de_salida)
        registros_con_tiempo.append({'registro': registro, 'tiempo_transcurrido': tiempo_transcurrido})

    listado = {'registros': registros_con_tiempo}
    return render(request, 'interfaz_salida.html',listado)

def calcular_tiempo_transcurrido(hora_entrada, hora_salida):
    ahora = datetime.now().time()  # Obtiene la hora actual
    tiempo_transcurrido = datetime.combine(datetime.today(), ahora) - datetime.combine(datetime.today(), hora_entrada)
    
    # Formatea el tiempo transcurrido para que sea más legible
    horas, segundos = divmod(tiempo_transcurrido.seconds, 3600)
    minutos, segundos = divmod(segundos, 60)

    tiempo_formateado = f"{horas}:{minutos:02}:{segundos:02}"
    return tiempo_formateado

def int_historial(request):
    return render(request, 'historia.html')
def int_configuration(request):
    return render(request, 'configuration.html')
def int_perfil(request):
    return render(request, 'perfil.html')


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
                parqueo_disponible = ParqueoDisponible.objects.first()
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

    try:
        with transaction.atomic():
            # Obtén el registro de vehículos por su ID y actualízalo
            registro_vehiculo = RegistroVehiculos.objects.get(pk=idregistrovehiculos)
            registro_vehiculo.Estado = 'I'
            registro_vehiculo.Hora_de_salida = hora_actual
            registro_vehiculo.save()

            # Incrementa la disponibilidad de parqueo
            parqueo_disponible = ParqueoDisponible.objects.first()
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
        cursor.execute("select TotalParqueoDisponible from interfaz_Entrada_parqueodisponible")           
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

"""---------grafica-----------------"""

"""def get_chart(_request):

    colors = ['blue', 'orange', 'red', 'black', 'yellow', 'green', 'magenta', 'lightblue', 'purple', 'brown']
    random_color = colors[randrange(0, (len(colors)-1))]

    serie = []
    counter = 0

    while (counter < 7):
        serie.append(randrange(100, 400))
        counter += 1

    chart = {
        'tooltip': {
            'show': True,
            'trigger': "axis",
            'triggerOn': "mousemove|click"
        },
        'xAxis': [
            {
                'type': "category",
                'data': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            }
        ],
        'yAxis': [
            {
                'type': "value"
            }
        ],
        'series': [
            {
                'data': serie,
                'type': "line",
                'itemStyle': {
                    'color': random_color
                },
                'lineStyle': {
                    'color': random_color
                }
            }
        ]
    }

    return JsonResponse(chart)"""



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


def obtener_anios(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT YEAR(fecha) AS Anio 
            FROM interfaz_Entrada_registrovehiculos
            ORDER BY Anio DESC
        """)
        anios = [row[0] for row in cursor.fetchall()]

    return JsonResponse({'anios': anios})


from django.http import JsonResponse
from django.db import connection

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

    resultados = sorted([{'Mes': row[0], 'Total': row[1]} for row in data], key=lambda x: x['Mes'])

    return JsonResponse({'resultados': resultados})

