# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import (CustomUserCreationForm ,CustomUserEditForm ,CustomAuthenticationForm)
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@csrf_protect
def home(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Registro exitoso! Puedes iniciar sesión ahora.')
            return redirect('usuarios:login')  # Redirigir a la página de inicio de sesión
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/home.html', {'form': form}) 
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
                return redirect('usuarios:perfil')
        else:
            print("Formulario no válido.")  # Para depuración
            print(form.errors)  # Mostrar errores del formulario
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

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)  # Usar el formulario con los datos del usuario
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('usuarios:perfil')  # Redirigir a la vista de perfil
    else:
        form = CustomUserCreationForm(instance=user)  # Cargar el formulario con los datos actuales del usuario

    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
def editar_perfil(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('usuarios:perfil')  # Redirige a la página de perfil después de guardar
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})