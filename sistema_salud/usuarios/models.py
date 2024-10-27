# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('paciente', 'Paciente'),
        ('profesional', 'Profesional de la Salud'),
    ]
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)  # Cambia esto para usar el atributo de clase
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
