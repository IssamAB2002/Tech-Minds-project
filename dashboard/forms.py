from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class ProfileCreation(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())