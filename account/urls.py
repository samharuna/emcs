from django.urls import path
from account import views
from account.views import ResetPasswordView, ResetPasswordConfirmView


urlpatterns = [
    path('sign/in/', views.sign_in, name='sign-in'),
    path('sign/up/', views.sign_up, name='sign-up'),
    path('sign/out/', views.sign_out, name='sign-out'),
    
    path('password/reset/', ResetPasswordView.as_view(), name='reset'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset-confirm'),
]





