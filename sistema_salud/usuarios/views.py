# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from sistema_salud.decorators import paciente_required
from .forms import CustomUserCreationForm, CustomUserEditForm, CustomAuthenticationForm
from .models import CustomUser
from django.core.paginator import Paginator
from citas.models import Cita  

import json






@csrf_protect
def home(request):
    
    ciudades = ["Santiago", "Valparaiso", "Concepcion"]  # Ejemplo de ciudades
    comunas_por_ciudad = {
        "Santiago": ["Providencia", "Las Condes", "Ñuñoa"],
        "Valparaiso": ["Viña del Mar", "Reñaca", "Quilpue"],
        "Concepcion": ["Talcahuano", "San Pedro de la Paz", "Chiguayante"],
    }
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, "Registro exitoso. Por favor, inicia sesión.")
            return redirect("usuarios:login")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = CustomUserCreationForm()

    

    context = {
        "form": form,
        "ciudades": ciudades,
        "comunas_por_ciudad": json.dumps(comunas_por_ciudad),
    }

    return render(request, 'usuarios/home.html', context) 



@csrf_protect
def login_usuario(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '¡Inicio de sesión exitoso!')

                # Redirigir según el tipo de usuario
                if user.user_type == 'paciente':
                    return redirect('usuarios:perfil')  # Redirige a la vista específica para pacientes
                elif user.user_type == 'profesional':
                    return redirect('usuarios:perfil')  # Redirige a la vista específica para profesionales
                else:
                    return redirect('usuarios:home')  # Redirige a perfil por defecto

            else:
                messages.error(request, 'Credenciales inválidas. Intenta nuevamente.')

        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)  # Mostrar errores en el front-end
    else:
        form = CustomAuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required  # Asegúrate de que el usuario esté autenticado
def perfil_usuario(request):
    user = request.user  # Obtén el usuario actual
    if user.user_type == 'paciente':
        # Contar las citas programadas para el paciente
        total_citas = Cita.objects.filter(paciente=user).count()
        total_consultas_realizadas = Cita.objects.filter(paciente=user, estado_cita='realizada').count()
        total_notificaciones_pendientes = Cita.objects.filter(paciente=user, estado_cita='pendiente').count()
    elif user.user_type == 'profesional':
        # Contar las citas programadas para el profesional
        total_citas = Cita.objects.filter(profesional=user).count()
        total_consultas_realizadas = Cita.objects.filter(profesional=user, estado_cita='realizada').count()
        total_notificaciones_pendientes = Cita.objects.filter(profesional=user, estado_cita='pendiente').count()
    else:
        total_citas = 0  

    
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)  # Usar el formulario con los datos del usuario
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('usuarios:perfil')  # Redirigir a la vista de perfil
    else:
        form = CustomUserCreationForm(instance=user)  # Cargar el formulario con los datos actuales del usuario

    context = {
        'form':form,
        'user': user,
        'total_citas': total_citas,
        'total_consultas_realizadas': total_consultas_realizadas,
        'total_notificaciones_pendientes': total_notificaciones_pendientes,
    }

    return render(request, 'usuarios/perfil.html', context)


@login_required
def editar_perfil(request):
    
    user = request.user

    # Obtener la ciudad y comuna seleccionada del GET
    ciudad = request.GET.get('ciudad', user.ciudad)  # Valor predeterminado es la ciudad del usuario
    comuna = request.GET.get('comuna', user.comuna)  # Valor predeterminado es la comuna del usuario

    # Obtener las ciudades y comunas para el formulario
    ciudades_disponibles = CustomUser.objects.values_list('ciudad', flat=True).distinct()
    comunas_disponibles = CustomUser.objects.filter(ciudad=ciudad).values_list('comuna', flat=True).distinct() if ciudad else []

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('usuarios:perfil')  # Redirige a la página de perfil
    else:
        form = CustomUserEditForm(instance=user)

    context = {
        "form": form,
        "ciudad": ciudad,
        "comuna": comuna,
        "ciudades_disponibles": ciudades_disponibles,
        "comunas_disponibles": comunas_disponibles,  # Comunas relacionadas con la ciudad seleccionada
    }

    return render(request, 'usuarios/editar_perfil.html', context)


@login_required
@paciente_required
def buscar_profesionales(request):
    ciudad = request.GET.get('ciudad', '')
    comuna = request.GET.get('comuna', '')
    especialidad = request.GET.get('q', '')

    # Obtener las ciudades y comunas para el formulario
    ciudades_disponibles = CustomUser.objects.values_list('ciudad', flat=True).distinct()
    comunas_disponibles = CustomUser.objects.filter(ciudad=ciudad).values_list('comuna', flat=True).distinct() if ciudad else []

    # Crear un queryset base
    profesionales = CustomUser.objects.filter(user_type='profesional')

    # Aplicar filtros
    if especialidad:
        profesionales = profesionales.filter(specialties__icontains=especialidad)
    if ciudad:
        profesionales = profesionales.filter(ciudad=ciudad)
    if comuna:
        profesionales = profesionales.filter(comuna=comuna)

    # Paginación
    paginator = Paginator(profesionales, 10)  # Mostrar 10 profesionales por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profesionales': page_obj,
        'ciudades_disponibles': ciudades_disponibles,
        'comunas_disponibles': comunas_disponibles,
        'ciudad': ciudad,
        'comuna': comuna,
        'especialidad': especialidad,
    }
    return render(request, 'usuarios/buscar_profesionales.html', context)



