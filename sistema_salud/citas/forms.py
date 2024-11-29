# citas/forms.py
from django import forms
from .models import Cita, CustomUser
from django.core.exceptions import ValidationError
from datetime import date

class CitaForm(forms.ModelForm):
    hora_inicio = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
        })
    )
    
    class Meta:
        model = Cita
        fields = ['fecha', 'profesional', 'hora_inicio', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'profesional': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'mt-1 block w-full bg-gray-100 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Describa brevemente el motivo de la cita',
            }),
        }

    def __init__(self, *args, horas_disponibles=None, profesional=None, fecha=None, **kwargs):
        """
        Inicializa el formulario con horarios dinámicos y profesionales disponibles.
        """
        super().__init__(*args, **kwargs)

        # Filtra los profesionales disponibles en el campo 'profesional'
        self.fields['profesional'].queryset = CustomUser.objects.filter(user_type='profesional')

        # Maneja los horarios
        self._set_horarios_disponibles(horas_disponibles, profesional, fecha)

    def _set_horarios_disponibles(self, horas_disponibles, profesional, fecha):
        """
        Configura las opciones de 'hora_inicio' según los horarios disponibles y ocupados.
        """
        # Si no se proporcionaron horarios base, usa una lista vacía
        horarios_base = horas_disponibles or []
        horarios_ocupados = []

        if profesional and fecha:
            # Obtiene los horarios ocupados del profesional en esa fecha
            horarios_ocupados = Cita.objects.filter(
                profesional=profesional,
                fecha=fecha
            ).exclude(estado_cita__in=['cancelada_paciente', 'cancelada_profesional']) \
             .values_list('hora_inicio', flat=True)

        # Genera las opciones con etiquetas indicativas
        self.fields['hora_inicio'].choices = [
            (hora, f"{hora} (ocupado)" if hora in horarios_ocupados else hora)
            for hora in horarios_base
        ]

    def clean_fecha(self):
        """
        Valida que la fecha no sea en el pasado.
        """
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < date.today():
            raise ValidationError("La fecha no puede ser en el pasado.")
        return fecha
    
class BloquearHorarioForm(forms.ModelForm):
    hora_inicio = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Cita
        fields = ['fecha', 'hora_inicio', 'es_bloqueado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'es_bloqueado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        horas_disponibles = kwargs.pop('horas_disponibles', [])
        super().__init__(*args, **kwargs)
        self.fields['hora_inicio'].choices = [(hora, hora) for hora in horas_disponibles]