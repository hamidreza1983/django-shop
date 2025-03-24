from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
    

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class SignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

class SetAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['profile', 'province', 'city', 'complete_address', 'postal_code', 'receiver']
