from django.db import models
from django.db.models.fields import CharField,AutoField,TimeField,DateField

# Create your models here.
class HistorialYEstadisticas(models.Model):
    idhistorial_y_estadisticas = models.AutoField(primary_key=True)
    Tipo_vehiculo = models.CharField(max_length=45)
    total = models.IntegerField()

    def __str__(self):
        return f'HistorialYEstadisticas #{self.idhistorial_y_estadisticas}'
    
class RegistroVehiculos(models.Model):
    idregistrovehiculos = models.AutoField(primary_key=True)
    Tipo_de_vehiculo = models.CharField(max_length=45)
    fecha = models.DateField()
    Hora_de_entrada = models.TimeField()
    Hora_de_salida = models.TimeField()
    Usuario = models.CharField(max_length=45)
    Estado = models.CharField(max_length=1)
    Id_tabla_historial = models.ForeignKey(
        HistorialYEstadisticas,
        
        models.RESTRICT,  # On Delete RESTRICT
        db_column='Id_tabla_historial'  # Nombre de la columna en la base de datos
    )

    def __str__(self):
        return f'RegistroVehiculos #{self.idregistrovehiculos}'
    

    


