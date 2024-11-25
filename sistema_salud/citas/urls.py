from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('paciente/citas/', views.lista_citas_paciente, name='lista_citas_paciente'),
    path('paciente/agendar/', views.agendar_cita, name='agendar_cita'),
    path('profesional/citas/', views.lista_citas_profesional, name='lista_citas_profesional'),
     path('cambiar_estado/<int:cita_id>/<str:nuevo_estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
     path('agendar-cita/<str:profesional>/', views.agendar_cita, name='agendar_cita'),
  
]

