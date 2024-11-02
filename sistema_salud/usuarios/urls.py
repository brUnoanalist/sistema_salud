# usuarios/urls.py
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path


app_name = 'usuarios'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'), 
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('buscar-profesionales/', views.buscar_profesionales, name='buscar_profesionales'),
]
     # Recuperación de contraseña
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

