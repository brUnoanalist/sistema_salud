# Generated by Django 5.1.2 on 2024-11-04 14:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0006_remove_cita_estado_cita_estado_cita'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='cita',
            index=models.Index(fields=['fecha'], name='citas_cita_fecha_d72c2d_idx'),
        ),
        migrations.AddIndex(
            model_name='cita',
            index=models.Index(fields=['estado_cita'], name='citas_cita_estado__701af3_idx'),
        ),
    ]
