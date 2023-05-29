from django.http import HttpResponse
from django.shortcuts import render, redirect    
    

def unauthenticated_users(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return  view_function(request, *args, **kwargs)
    return wrapper_function


def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            print('Working', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return render(request, 'backend/error_page.html', {"key":"Authorization Page"})
        return wrapper_function
    return decorator

