from django.db import models
from usuarios.models import CustomUser
from datetime import datetime, timedelta
import datetime as dt


class CitaManager(models.Manager):
    def pendientes(self):
        """Devuelve todas las citas pendientes."""
        return self.filter(estado_cita='pendiente')

    def confirmadas(self):
        """Devuelve todas las citas confirmadas."""
        return self.filter(estado_cita='confirmada')

    def canceladas(self):
        """Devuelve todas las citas canceladas."""
        return self.filter(estado_cita__in=[
            'cancelada_paciente', 'cancelada_profesional'
        ])


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
    hora_inicio = models.CharField(max_length=10)  # Formato HH:MM
    es_bloqueado = models.BooleanField(default=False)
    duracion = models.IntegerField()  # Duración de la cita en minutos
    estado_cita = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)

    objects = CitaManager()  # Usar el manager personalizado

    def __str__(self):
        return f'Cita {self.id} - {self.paciente.full_name} con {self.profesional.full_name}'

    @property
    def hora_fin(self):
        """Calcula la hora de finalización de la cita."""
        hora_inicio_obj = dt.datetime.strptime(self.hora_inicio, '%H:%M').time()
        return (datetime.combine(self.fecha, hora_inicio_obj) + timedelta(minutes=self.duracion)).time()

    @property
    def esta_en_el_pasado(self):
        """Verifica si la cita está en el pasado."""
        return datetime.combine(self.fecha, self.hora_fin) < datetime.now()

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
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['estado_cita']),
        ]
