from django.contrib import admin
from . models import HistorialYEstadisticas,RegistroVehiculos,EstadiaTotal,ParqueoDisponible
# Register your models here.
admin.site.register(HistorialYEstadisticas),
admin.site.register(RegistroVehiculos),
admin.site.register(EstadiaTotal),
admin.site.register(ParqueoDisponible),
