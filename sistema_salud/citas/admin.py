from django.contrib import admin
from .models import Cita, CitaManager
from usuarios.models import CustomUser  # Importar el modelo CustomUser


class CitaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "paciente":
            # Filtra para que solo se muestren pacientes
            kwargs["queryset"] = CustomUser.objects.filter(user_type='paciente')
        elif db_field.name == "profesional":
            # Filtra para que solo se muestren profesionales de salud
            kwargs["queryset"] = CustomUser.objects.filter(user_type='profesional')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Cita, CitaAdmin  )

