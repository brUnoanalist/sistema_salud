# sistema_salud/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from usuarios.views import home  # Asegúrate de importar la vista home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Ruta para la página de inicio
    path('usuarios/', include('usuarios.urls')),  # App de usuarios
    path('citas/', include('citas.urls')), # App de citas
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)