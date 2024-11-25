# citas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Cita,CustomUser
from .forms import CitaForm, BloquearHorarioForm



# Paciente: Ver y agendar citas
@login_required
def lista_citas_paciente(request):
    citas = Cita.objects.filter(paciente=request.user)
    return render(request, 'citas/lista_citas_paciente.html', {'citas': citas})

# Profesional: Ver citas asignadas
@login_required
def lista_citas_profesional(request):
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    # Filtrar las citas del profesional actual
    citas_hoy = Cita.objects.filter(profesional=request.user, fecha=today).order_by('hora_inicio')
    citas_manana = Cita.objects.filter(profesional=request.user, fecha=tomorrow).order_by('hora_inicio')
    proximas_citas = Cita.objects.filter(profesional=request.user, fecha__gt=tomorrow).order_by('fecha', 'hora_inicio')

    context = {
        'citas_hoy': citas_hoy,
        'citas_manana': citas_manana,
        'proximas_citas': proximas_citas,
    }
    return render(request, 'citas/lista_citas_profesional.html', context)




def agendar_cita(request):
    horas_disponibles = ['08:00', '08:30', '09:00', '09:30', '10:00', '11:00', '11:30', '12:00', '12:30', '14:00']
    
    # Obtener el ID del profesional desde la URL
    profesional_id = request.GET.get('profesional_id')
    profesional = None
    
    if profesional_id:
        # Obtener el objeto de profesional basado en el ID pasado
        profesional = get_object_or_404(CustomUser, id=profesional_id, user_type='profesional')

    if request.method == 'POST':
        form = CitaForm(request.POST, horas_disponibles=horas_disponibles)
        if form.is_valid():
            # Comprobar si ya existe una cita en esa fecha y hora con el profesional
            if Cita.objects.filter(
                profesional=form.cleaned_data['profesional'],
                fecha=form.cleaned_data['fecha'],
                hora_inicio=form.cleaned_data['hora_inicio']
            ).exists():
                form.add_error('hora_inicio', 'Esta hora ya está ocupada por otra cita.')
            else:
                # Guardar la cita si es válida y no hay conflicto de horarios
                cita = Cita(
                    paciente=request.user,
                    profesional=form.cleaned_data['profesional'],
                    fecha=form.cleaned_data['fecha'],
                    hora_inicio=form.cleaned_data['hora_inicio'],
                    descripcion=form.cleaned_data.get('descripcion', ''),
                    duracion=30,
                    estado_cita='pendiente',
                )
                cita.save()
                return redirect('citas:lista_citas_paciente')
    else:
        # Configurar el formulario con el profesional preseleccionado
        form = CitaForm(
            horas_disponibles=horas_disponibles,
            initial={'profesional': profesional} if profesional else None
        )

    return render(request, 'citas/agendar_cita.html', {'form': form, 'horas_disponibles': horas_disponibles})


@login_required
def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)

    if nuevo_estado == 'confirmada':
        cita.confirmar()
    elif nuevo_estado == 'cancelada_paciente':
        cita.cancelar_por_paciente()
    elif nuevo_estado == 'cancelada_profesional':
        cita.cancelar_por_profesional()
    
    # Redirigir al usuario de vuelta a la lista de citas
    return redirect('citas:lista_citas_paciente' if request.user == cita.paciente else 'citas:lista_citas_profesional')

@login_required
def bloquear_horario(request):
    if request.method == 'POST':
        form = BloquearHorarioForm(request.POST)
        if form.is_valid():
            bloqueo = form.save(commit=False)
            bloqueo.profesional = request.user  # Asumimos que el usuario autenticado es el profesional
            bloqueo.es_bloqueado = True
            bloqueo.save()
            return redirect('profesional_dashboard')  # Redirige al dashboard del profesional o donde prefieras
    else:
        form = BloquearHorarioForm()
    
    return render(request, 'citas/bloquear_horario.html', {'form': form})