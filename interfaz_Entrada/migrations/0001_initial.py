# Generated by Django 4.2.5 on 2023-09-23 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialYEstadisticas',
            fields=[
                ('idhistorial_y_estadisticas', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo_vehiculo', models.CharField(max_length=45)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RegistroVehiculos',
            fields=[
                ('idregistrovehiculos', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo_de_vehiculo', models.CharField(max_length=45)),
                ('fecha', models.DateField()),
                ('Hora_de_entrada', models.TimeField()),
                ('Hora_de_salida', models.TimeField()),
                ('Usuario', models.CharField(max_length=45)),
                ('Estado', models.CharField(max_length=1)),
                ('Id_tabla_historial', models.ForeignKey(db_column='Id_tabla_historial', on_delete=django.db.models.deletion.RESTRICT, to='interfaz_Entrada.historialyestadisticas')),
            ],
        ),
    ]
