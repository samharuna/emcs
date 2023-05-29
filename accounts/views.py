from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from backend.models import Profile
from accounts.forms import RegisterForm, LoginForm, SignInForm, SignUpForm
from backend.decorators import unauthenticated_users

# Create your views here.

@unauthenticated_users
def log_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Account creation for '{username}' was successful, Login now")

            group = Group.objects.get(name="customer")
            user.groups.add(group)
           
            return redirect('log_in')
        else:
            messages.info(request, 'Your Registration was not successful')
    else:
        form = RegisterForm()
    context = {'key':'Register', 'form': form}
    return render(request, 'accounts/sign_up.html', context)

@unauthenticated_users
def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            form.errors
    else:
        form = LoginForm()
    context = {'key':'Log In', 'form': form}
    return render(request, 'accounts/sign_in.html', context)

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('log_in')
    

class ResetPasswordConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_message = "Your new password has been set successfully. You may go ahead and log in now." 
    success_url = reverse_lazy('log_in')




def logupapp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Registration for '{username}' was successful, Login now")

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            return redirect('loginapp')
        else:
            messages.info(request, 'Your Registration was not successful')
    else:
        form = SignUpForm()
    context = {'key':'Register', 'signupForm':form}
    return render(request, 'accounts/signup.html', context)

def loginapp(request):
    if request.method == "POST":
        form = SignInForm(request.POST or None)
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('post')
        else:
            form.errors
    else:
        form = SignInForm()
    context = {'key':'Login', 'signinForm':form}
    return render(request, 'accounts/signin.html', context)


@login_required(login_url='log_in')
def logoutapp(request):
    logout(request)
    return redirect('post')



class PasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'blog/password_reset.html'
    email_template_name = 'blog/password_reset_email.html'
    subject_template_name = 'blog/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('loginapp')
    

class PasswordConfirmResetView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'blog/password_reset_confirm.html'
    success_message = "Your new password has been set successfully. You may go ahead and log in now." 
    success_url = reverse_lazy('loginapp')



def handle_not_found(request, exception):
    context = {'key':'Page Not Found Error'}
    return render(request, 'accounts/error_404.html', context)


def internal_server(request):
    context = {'key':'Internal Server Error'}
    return render(request, 'accounts/error_500.html', context)


