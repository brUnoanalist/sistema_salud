# usuarios/urls.py

from .views import (login_usuario,home,perfil_usuario,editar_perfil,
                    logout_view)
from django.urls import path


app_name = 'usuarios'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_usuario, name='perfil'), 
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
     # Recuperación de contraseña
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]