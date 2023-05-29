from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from accounts.models import User


class RegisterForm(UserCreationForm):
    username    = forms.CharField(max_length=100, label='Username', widget=forms.TextInput(attrs={'placeholder':'Username', 'type': 'text'}))
    email       = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'type':'email'}))
    first_name  = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'placeholder':'First Name', 'type': 'text'}))
    last_name   = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'type': 'text'}))
    password1   = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'type':'password'}))
    password2   = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'type':'password'}))
    
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        error_class = 'error'
    

class LoginForm(forms.ModelForm):
    email       = forms.EmailField(max_length=100, label='Email Address', widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'type':'email'}))
    password   = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'type':'password', 'id':'password'}))

    class Meta:
        model = User
        fields = ['email', 'password']
        error_class = 'error'

    def clean(self):
        if self.is_valid():
            email       = self.cleaned_data['email']
            password    = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login Credentials')


class ChangePasswordForm(PasswordChangeForm):
    old_password    = forms.CharField(max_length=100, label='Old Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter Old Password Here ...', 'type':'password'}))
    new_password1   = forms.CharField(max_length=100, label='New Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter New Password Here ...', 'type':'password'}))
    new_password2   = forms.CharField(max_length=100, label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter Confirm New Password Here ...', 'type':'password'}))
   
    class Meta(PasswordChangeForm):
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        error_class = 'error'


class SignInForm(forms.ModelForm):
    email       = forms.EmailField(max_length=100, label='', widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'type':'email', 'id':'email'}))
    password   = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'type':'password', 'id':'password'}))

    class Meta:
        model = User
        fields = ['email', 'password']
        error_class = 'error'

    def clean(self):
        if self.is_valid():
            email       = self.cleaned_data['email']
            password    = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login Credentials')


class SignUpForm(UserCreationForm):
    username    = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'Username', 'type': 'text', 'id':'username'}))
    first_name  = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'First Name', 'type': 'text'}))
    last_name   = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'type': 'text'}))
    email       = forms.EmailField(max_length=100, label='', widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'type':'email', 'id':'email'}))
    password1   = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'type':'password', 'id':'password1'}))
    password2   = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'type':'password', 'id':'password2'}))
    
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        error_class = 'error'