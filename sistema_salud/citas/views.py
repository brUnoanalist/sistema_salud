# citas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Cita,CustomUser
from .forms import CitaForm, BloquearHorarioForm
from datetime import datetime
from django.http import JsonResponse



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
    citas_manana = Cita.objects.filter(
    profesional=request.user,
    fecha=tomorrow,
    estado_cita__in=['pendiente','confirmada']
    ).order_by('hora_inicio')
    proximas_citas = Cita.objects.filter(profesional=request.user, fecha__gt=today, estado_cita='confirmada')
    cantidad_citas = proximas_citas.count() 
    print(cantidad_citas)
    citas_canceladas = Cita.objects.filter(profesional=request.user, estado_cita__in=['cancelada_paciente','cancelada_paciente'])
    

    context = {
        'citas_hoy': citas_hoy,
        'citas_manana': citas_manana,
        'cantidad_citas': cantidad_citas,
        'citas_canceladas':citas_canceladas,
        'proximas_citas':proximas_citas
    }
    return render(request, 'citas/lista_citas_profesional.html', context)

def citas_view(request):
    

    # Filtrar citas activas (futuras)
    citas_activas = Cita.objects.filter(profesional=request.user, fecha__gte=datetime.now(), estado_cita="confirmada")

    # Segregar citas activas por estado
    citas_pendientes = Cita.objects.filter(estado_cita="pendiente")  # Aún no confirmadas
    citas_confirmadas = Cita.objects.filter(fecha__gte=datetime.now(),estado_cita="confirmada")  # Confirmadas por el usuario o sistema

    # Citas pasadas
    citas_pasadas = Cita.objects.filter(profesional=request.user, fecha__lt=datetime.now())
    citas_completadas = Cita.objects.filter(estado_cita="completada")
    citas_canceladas = Cita.objects.filter(profesional=request.user, estado_cita__in=['cancelada_paciente','cancelada_paciente'])

    context = {
        'citas_pasadas':citas_pasadas,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
    }
    return render(request, 'citas/citas.html', context)


def agendar_cita(request):
    horas_disponibles = ['08:00', '08:30', '09:00', '09:30', '10:00', '11:00', '11:30', '12:00', '12:30', '14:00']

    # Obtener el ID del profesional desde los parámetros GET
    profesional_id = request.GET.get('profesional_id')
    profesional = None
    fecha = None

    # Si se recibe un ID de profesional, obtenemos el profesional desde la base de datos
    if profesional_id:
        profesional = get_object_or_404(CustomUser, id=profesional_id, user_type='profesional')

    # Procesar el formulario cuando se envía con POST
    if request.method == 'POST':
        form = CitaForm(request.POST, horas_disponibles=horas_disponibles, profesional=profesional, fecha=request.POST.get('fecha'))
        
        # Validar el formulario
        if form.is_valid():
            # Obtener los datos del formulario
            cita_data = form.cleaned_data
            cita_profesional = cita_data['profesional']
            cita_fecha = cita_data['fecha']
            cita_hora_inicio = cita_data['hora_inicio']

            # Verificar si ya existe una cita para ese profesional, fecha y hora
            if Cita.objects.filter(profesional=cita_profesional,
                                   fecha=cita_fecha,
                                   hora_inicio=cita_hora_inicio).exclude(estado_cita__in=['cancelada_paciente', 'cancelada_profesional']).exists():
                form.add_error('hora_inicio', 'Esta hora ya está ocupada por otra cita.')
            else:
                # Si no hay conflicto, guardamos la cita
                cita = form.save(commit=False)
                cita.paciente = request.user
                cita.estado_cita = 'pendiente'

                # Asignar duración predeterminada si no se pasa
                if not cita.duracion:
                    cita.duracion = 30

                cita.save()
                return redirect('citas:lista_citas_paciente')
    else:
        # Si el método no es POST, inicializamos el formulario con la fecha recibida
        fecha = request.GET.get('fecha')
        form = CitaForm(
            horas_disponibles=horas_disponibles,
            initial={'profesional': profesional} if profesional else None,
            fecha=fecha
        )

    return render(request, 'citas/agendar_cita.html', {'form': form, 'horas_disponibles': horas_disponibles})




@login_required
def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)

    if nuevo_estado == 'confirmada':
        cita.confirmar()
    elif nuevo_estado == 'completada':
        cita.completada()    
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