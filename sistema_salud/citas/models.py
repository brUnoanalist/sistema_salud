from django.db import models
from usuarios.models import CustomUser
from datetime import datetime, timedelta 
import datetime as dt 

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada_paciente', 'Cancelada por el Paciente'),
        ('cancelada_profesional', 'Cancelada por el Profesional'),
    ]
    paciente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citas_paciente')
    profesional = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citas_profesional')
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    hora_inicio = models.CharField(max_length=10) 
    es_bloqueado = models.BooleanField(default=False) 
    duracion = models.IntegerField()  # Duración de la cita en minutos
    estado_cita = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f'Cita {self.id} - {self.paciente.full_name} con {self.profesional.full_name}'

    @property
    def hora_fin(self):
        """Calcula la hora de finalización de la cita."""
        hora_inicio_obj = dt.datetime.strptime(self.hora_inicio, '%H:%M').time()
        return (datetime.combine(self.fecha, hora_inicio_obj) + timedelta(minutes=self.duracion)).time()

    def cancelar_por_paciente(self):
        """Cancela la cita por el paciente."""
        self.estado_cita = 'cancelada_paciente'
        self.save()

    def cancelar_por_profesional(self):
        """Cancela la cita por el profesional."""
        self.estado_cita = 'cancelada_profesional'
        self.save()

    def confirmar(self):
        """Confirma la cita por el profesional."""
        self.estado_cita = 'confirmada'
        self.save()

    class Meta:
        ordering = ['fecha']
