from django.urls import path
from backend import views

urlpatterns = [
     path('dashboard/', views.dashboard, name='dashboard'),
     
     path('staffprofiles/', views.staffprofiles, name='staffprofiles'),
     path('profiles/', views.profiles, name='profiles'),
     path('profile/<str:username>/', views.profile, name='profile'),
     path('edit/profile/', views.edit_profile, name='edit-profile'),
     path('edit/user/', views.edit_user, name='edit-user'),
     path('change/password/', views.change_password, name='change-password'),
     path('change/picture/', views.change_picture, name='change-picture'),
     
     path('super/user/', views.super_user, name='superuser'),
     path('view/super/users/', views.view_superuser, name='view-superuser'),
     path('edit/super/user/<slug:slug>/', views.edit_superuser, name='edit-superuser'),
    
     path('staff/user/', views.staff_user, name='staffuser'),
     path('view/staff/users/', views.view_staffuser, name='view-staffuser'),
     path('edit/staff/users/<slug:slug>/', views.edit_staffuser, name='edit-staffuser'),
     
     path('view/users/', views.view_user, name='view-user'),
     
     path('banned/users/', views.view_banned, name='view-banned'),
     path('edit/banned/users/<slug:slug>/', views.edit_banneduser, name='edit-banneduser'),
     
     path('view/all/users/', views.all_user, name='all-user'),
     path('edit/all/users/<slug:slug>/', views.edit_alluser, name='edit-alluser'),
     path('delete/all/users/<slug:slug>/', views.delete_alluser, name='delete-alluser'),
     
     path('add/about/', views.add_about, name='add-about'),
     path('view/about/', views.view_about, name='view-about'),
     path('edit/about/<slug:slug>/', views.edit_about, name='edit-about'),
     path('delete/about/<slug:slug>/', views.delete_about, name='delete-about'),
     
     path('add/advert/', views.add_advert, name='add-advert'),
     path('view/advert/', views.view_advert, name='view-advert'),
     path('edit/advert/<slug:slug>/', views.edit_advert, name='edit-advert'),
     path('delete/advert/<slug:slug>/', views.delete_advert, name='delete-advert'),
     
     path('add/blog/', views.add_blog, name='add-blog'),
     path('view/blog/', views.view_blog, name='view-blog'),
     path('edit/blog/<slug:slug>/', views.edit_blog, name='edit-blog'),
     path('delete/blog/<slug:slug>/', views.delete_blog, name='delete-blog'),
     
     path('blog/approve_page/', views.approve_blog_view, name='approve-blogview'),
     path('approve/blog/<slug:slug>/', views.approve_blog, name='approve-blog'),
     path('disapprove/blog/<slug:slug>/', views.disapprove_blog, name='disapprove-blog'),
     
     path('blog/approve/', views.blog_approve, name='blog-approve'),
     path('blog/disapprove/', views.blog_disapprove, name='blog-disapprove'),
     path('blog/pending/', views.blog_pending, name='blog-pending'),
     path('status/blog/<slug:slug>/', views.status_blog, name='status-blog'),
     
     
     path('add/career/', views.add_career, name='add-career'),
     path('view/career/', views.view_career, name='view-career'),
     path('edit/career/<slug:slug>/', views.edit_career, name='edit-career'),
     path('delete/career/<slug:slug>/', views.delete_career, name='delete-career'),
     
     path('add/category/', views.add_category, name='add-category'),
     path('view/category/', views.view_category, name='view-category'),
     path('edit/category/<slug:slug>/', views.edit_category, name='edit-category'),
     path('delete/category/<slug:slug>/', views.delete_category, name='delete-category'),
     
     path('view/contact/', views.view_contact, name='view-contact'),
     path('edit/contact/<slug:slug>/', views.edit_contact, name='edit-contact'),
     path('delete/contact/<slug:slug>/', views.delete_contact, name='delete-contact'),
     
     path('add/detail/', views.add_detail, name='add-detail'),
     path('view/detail/', views.view_detail, name='view-detail'),
     path('edit/detail/<slug:slug>/', views.edit_detail, name='edit-detail'),
     path('delete/detail/<slug:slug>/', views.delete_detail, name='delete-detail'),
     
     path('add/service/', views.add_service, name='add-service'),
     path('view/service/', views.view_service, name='view-service'),
     path('edit/service/<slug:slug>/', views.edit_service, name='edit-service'),
     path('delete/service/<slug:slug>/', views.delete_service, name='delete-service'),
     
     path('add/statement/', views.add_statement, name='add-statement'),
     path('view/statement/', views.view_statement, name='view-statement'),
     path('edit/statement/<slug:slug>/', views.edit_statement, name='edit-statement'),
     path('delete/statement/<slug:slug>/', views.delete_statement, name='delete-statement'),
     
     path('add/tag/', views.add_tag, name='add-tag'),
     path('view/tag/', views.view_tag, name='view-tag'),
     path('edit/tag/<slug:slug>/', views.edit_tag, name='edit-tag'),
     path('delete/tag/<slug:slug>/', views.delete_tag, name='delete-tag'),
     
     path('add/testimonial/', views.add_testimonial, name='add-testimonial'),
     path('view/testimonial/', views.view_testimonial, name='view-testimonial'),
     path('edit/testimonial/<slug:slug>/', views.edit_testimonial, name='edit-testimonial'),
     path('delete/testimonial/<slug:slug>/', views.delete_testimonial, name='delete-testimonial'),
     
     path('add/news/', views.add_news, name='add-news'),
     path('view/news/', views.view_news, name='view-news'),
     path('edit/news/<slug:slug>/', views.edit_news, name='edit-news'),
     path('delete/news/<slug:slug>/', views.delete_news, name='delete-news'),
     
     path('add/header/', views.add_header, name='add-header'),
     path('view/header/', views.view_header, name='view-header'),
     path('edit/header/<slug:slug>/', views.edit_header, name='edit-header'),
     path('delete/header/<slug:slug>/', views.delete_header, name='delete-header'),
     
     path('add/footer/', views.add_footer, name='add-footer'),
     path('view/footer/', views.view_footer, name='view-footer'),
     path('edit/footer/<slug:slug>/', views.edit_footer, name='edit-footer'),
     path('delete/footer/<slug:slug>/', views.delete_footer, name='delete-footer'),
     
     path('add/faq/', views.add_faq, name='add-faq'),
     path('view/faq/', views.view_faq, name='view-faq'),
     path('edit/faq/<slug:slug>/', views.edit_faq, name='edit-faq'),
     path('delete/faq/<slug:slug>/', views.delete_faq, name='delete-faq'),
     
     path('add/privacy/', views.add_privacy, name='add-privacy'),
     path('view/privacy/', views.view_privacy, name='view-privacy'),
     path('edit/privacy/<slug:slug>/', views.edit_privacy, name='edit-privacy'),
     path('delete/privacy/<slug:slug>/', views.delete_privacy, name='delete-privacy'),
          
     path('add/steps/', views.add_steps, name='add-steps'),
     path('view/steps/', views.view_steps, name='view-steps'),
     path('edit/steps/<slug:slug>/', views.edit_steps, name='edit-steps'),
     path('delete/steps/<slug:slug>/', views.delete_steps, name='delete-steps'),
     
     path('add/serviceheader/', views.add_serviceheader, name='add-serviceheader'),
     path('view/serviceheader/', views.view_serviceheader, name='view-serviceheader'),
     path('edit/serviceheader/<slug:slug>/', views.edit_serviceheader, name='edit-serviceheader'),
     path('delete/serviceheader/<slug:slug>/', views.delete_serviceheader, name='delete-serviceheader'),
     
     path('add/faqheader/', views.add_faqheader, name='add-faqheader'),
     path('view/faqheader/', views.view_faqheader, name='view-faqheader'),
     path('edit/faqheader/<slug:slug>/', views.edit_faqheader, name='edit-faqheader'),
     path('delete/faqheader/<slug:slug>/', views.delete_faqheader, name='delete-faqheader'),
     
     path('add/testimonialheader/', views.add_testimonialheader, name='add-testimonialheader'),
     path('view/testimonialheader/', views.view_testimonialheader, name='view-testimonialheader'),
     path('edit/testimonialheader/<slug:slug>/', views.edit_testimonialheader, name='edit-testimonialheader'),
     path('delete/testimonialheader/<slug:slug>/', views.delete_testimonialheader, name='delete-testimonialheader'),
     
     path('add/aboutheader/', views.add_aboutheader, name='add-aboutheader'),
     path('view/aboutheader/', views.view_aboutheader, name='view-aboutheader'),
     path('edit/aboutheader/<slug:slug>/', views.edit_aboutheader, name='edit-aboutheader'),
     path('delete/aboutheader/<slug:slug>/', views.delete_aboutheader, name='delete-aboutheader'),
     
     path('add/contactheader/', views.add_contactheader, name='add-contactheader'),
     path('view/contactheader/', views.view_contactheader, name='view-contactheader'),
     path('edit/contactheader/<slug:slug>/', views.edit_contactheader, name='edit-contactheader'),
     path('delete/contactheader/<slug:slug>/', views.delete_contactheader, name='delete-contactheader'),
     
     path('add/careerheader/', views.add_careerheader, name='add-careerheader'), 
     path('view/careerheader/', views.view_careerheader, name='view-careerheader'),
     path('edit/careerheader/<slug:slug>/', views.edit_careerheader, name='edit-careerheader'),
     path('delete/careerheader/<slug:slug>/', views.delete_careerheader, name='delete-careerheader'),
     
]