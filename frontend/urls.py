from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newsletter', views.newsletter, name='newsletter'),

    path('about/', views.about, name='about'),

    path('tags/<slug:slug>/', views.tags, name='tags'),
    path('category/<slug:slug>/', views.category, name='category'),
    
    path('service/', views.service, name='service'),
    path('service/detail/<slug:slug>/', views.service_detail, name='service_detail'),

    path('search/', views.search, name='search'),

    path('post/', views.post, name='post'),
    path('post/detail/<slug:slug>/', views.post_detail, name='post_detail'),
    path('add/reply/<int:post_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    
    path('likes/comment/<int:id>/', views.likes_comment, name='likes_comment'),
    path('dislikes/comment/<int:id>/', views.dislikes_comment, name='dislikes_comment'),

    path('likes/reply/<int:id>/', views.likes_reply, name='likes_reply'),
    path('dislikes/reply/<int:id>/', views.dislikes_reply, name='dislikes_reply'),

    path('team/', views.team, name='team'),
    path('team/detail/<slug:slug>/', views.team_detail, name='team_detail'),
    
    path('career/', views.career, name='career'),
    path('career/detail/<slug:slug>/', views.career_detail, name='career_detail'),
    
    path('faq/', views.faq, name='faq'),
    path('gallery/', views.gallery, name='gallery'),

    path('contact/us/', views.contact, name='contact_us'),

    path('blog/view/profile/', views.blog_viewprofile, name='blog_viewprofile'),
    path('blog/profile/<str:username>/', views.blog_profile, name='blog_profile'),
    path('blog/edit/name/', views.blog_editname, name='blog_editname'),
    path('blog/change/password/', views.blog_changepassword, name='blog_changepassword'),

    path('view/author/blog/', views.blog_view, name='blog_view'),
    path('form/author/blog/', views.blog_form, name='blog_form'),
    path('edit/author/blog/<slug:slug>/', views.blog_edit, name='blog_edit'),
    path('delete/author/blog/<slug:slug>/', views.blog_delete, name='blog_delete'),
    
]