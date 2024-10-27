# sistema_salud/urls.py
from django.contrib import admin
from django.urls import path, include
from usuarios.views import home  # Asegúrate de importar la vista home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Ruta para la página de inicio
    path('usuarios/', include('usuarios.urls')),  # App de usuarios
    path('citas/', include('citas.urls')), # App de citas
]

