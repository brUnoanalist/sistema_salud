# Generated by Django 5.1.2 on 2024-10-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0004_alter_cita_hora_inicio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cita',
            old_name='es_disponibilidad',
            new_name='es_bloqueado',
        ),
        migrations.AlterField(
            model_name='cita',
            name='hora_inicio',
            field=models.CharField(max_length=10),
        ),
    ]
