# Generated by Django 5.1.2 on 2024-10-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0002_cita_duracion_cita_es_disponibilidad_cita_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='fecha',
            field=models.DateField(),
        ),
    ]
