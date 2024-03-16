from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from account.forms import RegisterForm, LoginForm
from account.models import User


# Create your views here.
@force_maintenance_mode_off
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = LoginForm()
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
                    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Email Address does not Exist or Password is not valid')
    context = {'title':'Sign In', 'form':form}
    return render(request, 'account/auth/login.html', context)

@force_maintenance_mode_off
def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            email = form.cleaned_data['email']
            messages.success(request, f'Account creation for "{email}" was successful')
            return redirect('sign-in')
        else:
            form.errors
            messages.info(request, f'Account creation was not successful')
    else:
        form = RegisterForm()
    context = {'title':'Sign Up', 'form':form}
    return render(request, 'account/auth/register.html', context)

@login_required(login_url='sign-in')
def sign_out(request):
    logout(request)
    return redirect('sign-in')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password/password_reset.html'
    email_template_name = 'account/password/password_reset_email.html'
    subject_template_name = 'account/password/password_reset_subject.txt'
    success_message = "We've emailed you instructions for your password setting, " \
                      "if an account exists with the email you entered. You should receive them shortly, " \
                      "if you don't receive an email in your inbox, please check your spam folder."
    success_url = reverse_lazy('sign-in')
    
class ResetPasswordConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'account/password/password_reset_confirm.html'
    success_message = "Your new password has been set successfully. You may go ahead and log in now." 
    success_url = reverse_lazy('sign-in')