from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)

    USER_TYPE_CHOICES = [
        ('paciente', 'Paciente'),
        ('profesional', 'Profesional de la Salud'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone', 'user_type', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password1")
        password_confirmation = self.cleaned_data.get("password2")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class CustomUserEditForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'phone', 'user_type', 'profile_picture', 'bio','specialties')  # Añade o quita campos según sea necesario

    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)