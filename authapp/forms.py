from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Custom user creation form for admin use
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

# User profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
