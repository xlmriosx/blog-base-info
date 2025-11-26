from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo', required=True)
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    password1 = forms.CharField(label='Pass', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Pass Confirm', widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = Usuario
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]