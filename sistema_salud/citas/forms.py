# citas/forms.py
from django import forms
from .models import Cita, CustomUser

class CitaForm(forms.ModelForm):
    hora_inicio = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))  # Añadir clase form-control
    
    class Meta:
        model = Cita
        fields = ['fecha', 'profesional', 'hora_inicio', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profesional': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Ajustar descripción
        }

    def __init__(self, *args,  profesional_id=None, **kwargs):
        horas_disponibles = kwargs.pop('horas_disponibles', [])
        super().__init__(*args, **kwargs)
        self.fields['hora_inicio'].choices = [(hora, hora) for hora in horas_disponibles]
        self.fields['profesional'].queryset = CustomUser.objects.filter(user_type='profesional')
        if profesional_id:
            # Si se pasa un profesional, se selecciona como predeterminado
            self.fields['profesional'].initial = profesional_id
        self.fields['hora_inicio'].choices = [(hora, hora) for hora in horas_disponibles]
    
    
    def clean(self):
        cleaned_data = super().clean()
        profesional = cleaned_data.get('profesional')
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')

        if profesional and fecha and hora_inicio:
            # Verificar si ya existe una cita con el mismo profesional, fecha y hora
            if Cita.objects.filter(profesional=profesional, fecha=fecha, hora_inicio=hora_inicio).exists():
                self.add_error('hora_inicio', 'Esta hora ya está ocupada por otra cita.')
        
        return cleaned_data
    
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