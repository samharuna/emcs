from django.urls import path
from newsletter import views

urlpatterns = [
     path('newsletter/', views.newsletter, name='newsletter'),
     
     path('send/message/', views.send_message, name='send-message'),
     path('view/message/', views.view_message, name='view-message'),
     path('edit/message/<slug:slug>/', views.edit_message, name='edit-message'),
     path('delete/message/<slug:slug>/', views.delete_message, name='delete-message'),
     
     path('view/subscribers/', views.view_subscriber, name='view-subscriber'),
     path('edit/subscriber/<slug:slug>/', views.edit_subscriber, name='edit-subscriber'),
     path('delete/subscriber/<slug:slug>/', views.delete_subscriber, name='delete-subscriber'),
     
     path('send/mails/<slug:slug>/', views.send_mails, name='send-mails'),
     path('view/mails/', views.view_mails, name='view-mails'),
     path('detail/mails/<slug:slug>/', views.detail_mails, name='detail-mails'),
     path('delete/mails/<slug:slug>/', views.delete_mails, name='delete-mails'),
     
]