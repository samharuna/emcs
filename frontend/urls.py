from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('about/', views.about, name='about'),
    path('about/detail/<slug:slug>/', views.about_detail, name='about-detail'),
    
    path('career/', views.career, name='career'),
    path('career/detail/<slug:slug>/', views.career_detail, name='career_detail'),
    
    path('service/', views.service, name='service'),
    path('service/detail/<slug:slug>/', views.service_detail, name='service-detail'),
    
    path('tags/<slug:slug>/', views.tags, name='tags'),
    path('category/<slug:slug>/', views.category, name='category'),
    
    path('faq/', views.faq, name='faq'),
    
    path('contact/us/', views.contact, name='contact-us'),
    path('privacy/', views.privacy, name='privacy'),
    
    
]