from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import User


class RegisterForm(UserCreationForm):
    username    = forms.CharField(max_length=100, label='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username:', 'id':'username', 'type':'text', 'name':'username'}))
    first_name  = forms.CharField(max_length=100, label='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name:', 'id':'first_name', 'type':'text', 'name':'first_name'}))
    last_name   = forms.CharField(max_length=100, label='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name:', 'id':'last_name', 'type':'text', 'name':'last_name'}))
    email       = forms.EmailField(max_length=100, label='', required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address:', 'id':'email', 'type':'email', 'name':'email'}))
    password1   = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password:', 'id':'password', 'type':'password', 'name':'password'}))
    password2   = forms.CharField(label='', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Again:', 'id':'password', 'type':'password', 'name':'password'}))
    is_active   = forms.BooleanField(required=True, label='', initial=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox', 'id':'terms-conditions', 'name':'terms'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'password1', 'password2']
        
        
class LoginForm(AuthenticationForm):
    email       = forms.EmailField(max_length=100, label='Email Address', required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email Address:', 'id':'email', 'type':'email', 'name':'email'}))
    password    = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter your Password:', 'id':'password', 'type':'password', 'name':'password'}))
    class Meta:
        model = User
        fields = ['email', 'password']