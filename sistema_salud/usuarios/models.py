from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('paciente', 'Paciente'),
        ('profesional', 'Profesional de la Salud'),
    ]

   

    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    specialties = models.CharField(max_length=200, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ciudad']),
            models.Index(fields=['comuna']),
            models.Index(fields=['specialties']),
        ]

    def __str__(self):
        return self.full_name if self.full_name else self.username

    
