from django.http import HttpResponseForbidden

def paciente_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'paciente':
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return wrapper
