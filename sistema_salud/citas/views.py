# citas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita
from .forms import CitaForm, BloquearHorarioForm


# Paciente: Ver y agendar citas
@login_required
def lista_citas_paciente(request):
    citas = Cita.objects.filter(paciente=request.user)
    return render(request, 'citas/lista_citas_paciente.html', {'citas': citas})

# Profesional: Ver citas asignadas
@login_required
def lista_citas_profesional(request):
    citas = Cita.objects.filter(profesional=request.user)
    return render(request, 'citas/lista_citas_profesional.html', {'citas': citas})




def agendar_cita(request):
    horas_disponibles = ['08:00', '08:30', '09:00', '09:30', '10:00','11:00', '11:30', '12:00', '12:30', '14:00']  # Ejemplo de horas disponibles

    if request.method == 'POST':
        print("Método POST recibido.")
        print("Datos del formulario:", request.POST) 
        form = CitaForm(request.POST, horas_disponibles=horas_disponibles)  # Pasar horas disponibles aquí
        if form.is_valid():
            print("Formulario válido.")
            print("Datos del formulario:", form.cleaned_data)

            # Verificar si ya existe una cita para el profesional, fecha y hora
            if Cita.objects.filter(
                profesional=form.cleaned_data['profesional'],
                fecha=form.cleaned_data['fecha'],
                hora_inicio=form.cleaned_data['hora_inicio']
            ).exists():
                print("Error: Ya existe una cita agendada para esta hora.")
                form.add_error('hora_inicio', 'Esta hora ya está ocupada por otra cita.')
            else:
                # Crear el objeto Cita con los datos del formulario
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
                print("Cita guardada:", cita)
                
                # Redirigir a una página de éxito o mostrar un mensaje
                return redirect('home')

        if not form.is_valid():
            print("Errores del formulario:", form.errors)  
        else:
            print("Errores del formulario:", form.errors)
    else:
        print("Método GET recibido.")
        form = CitaForm(horas_disponibles=horas_disponibles)  # Pasar horas disponibles aquí

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