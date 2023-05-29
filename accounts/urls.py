from django.urls import path
from accounts.views import ResetPasswordView, ResetPasswordConfirmView, PasswordResetView, PasswordConfirmResetView

from accounts import views

urlpatterns = [
    path('sign/in/', views.log_in, name='log_in'),
    path('sign/up/', views.log_up, name='log_up'),
    path('sign/out/', views.log_out, name='log_out'),

    path('password/reset/', ResetPasswordView.as_view(), name='reset'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset_confirm'),

    path('log/in/', views.loginapp, name='loginapp'),
    path('new/account/', views.logupapp, name='logupapp'),
    path('log/out/', views.logoutapp, name='logoutapp'),

    path('reset/', PasswordResetView.as_view(), name='reset_pass'),
    path('done/<uidb64>/<token>/', PasswordConfirmResetView.as_view(), name='confirm_password'),
]
