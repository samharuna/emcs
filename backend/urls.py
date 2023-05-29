from django.urls import path
from backend import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('view/loan/', views.view_loan, name='view_loan'),
    path('add/loan/', views.add_loan, name='add_loan'),
    path('update/loan/<slug:slug>/', views.update_loan, name='update_loan'),
    path('edit/loan/<slug:slug>/', views.edit_loan, name='edit_loan'),
    path('payment/loan/<slug:slug>/', views.loan_payment, name='loan_payment'),
    path('delete/loan/<slug:slug>/', views.delete_loan, name='delete_loan'),
    path('applicant/loan/', views.applicant_loan, name='applicant_loan'),
    path('approve/loan/view/', views.approve_loan_view, name='approve_loan_view'),
    path('approve/loan/<slug:slug>/', views.approve_loan, name='approve_loan'),
    path('disapprove/loan/<slug:slug>/', views.disapprove_loan, name='disapprove_loan'),
    path('loan/pending/', views.loan_pending, name='loan_pending'),
    path('loan/approved/', views.loan_approved, name='loan_approved'),
    path('loan/disapproved/', views.loan_disapproved, name='loan_disapproved'),

    path('generate/pdf/loan/application/<int:loan_id>/', views.generate_loanpdf, name='generate_loanpdf'),
    path('generate/pdf/loan/payment/<int:loanpayment_id>/', views.generate_loanpaymentpdf, name='generate_loanpaymentpdf'),
    path('loan/pdf/view/', views.render_loanpdf_view, name='render_loanpdf_view'),

    path('view/loan/interest/', views.view_loaninterest, name='view_loaninterest'),
    path('add/loan/interest/', views.add_loaninterest, name='add_loaninterest'),
    path('update/loan/interest/<slug:slug>/', views.update_loaninterest, name='update_loaninterest'),
    path('delete/loan/interest/<slug:slug>/', views.delete_loaninterest, name='delete_loaninterest'),

    path('view/loan/duration/', views.view_loanduration, name='view_loanduration'),
    path('add/loan/duration/', views.add_loanduration, name='add_loanduration'),
    path('update/loan/duration/<slug:slug>/', views.update_loanduration, name='update_loanduration'),
    path('delete/loan/duration/<slug:slug>/', views.delete_loanduration, name='delete_loanduration'),

    path('view/investment/', views.view_investment, name='view_investment'),
    path('add/investment/', views.add_investment, name='add_investment'),
    path('update/investment/<slug:slug>/', views.update_investment, name='update_investment'),
    path('edit/investment/<slug:slug>/', views.edit_investment, name='edit_investment'),
    path('payment/investment/<slug:slug>/', views.investment_payment, name='investment_payment'),
    path('delete/investment/<slug:slug>/', views.delete_investment, name='delete_investment'),
    path('investor/investment/', views.investor_investment, name='investor_investment'),
    path('approve/investment/view/', views.approve_investment_view, name='approve_investment_view'),
    path('approve/investment/<slug:slug>/', views.approve_investment, name='approve_investment'),
    path('disapprove/investment/<slug:slug>/', views.disapprove_investment, name='disapprove_investment'),
    path('investment_pending/', views.investment_pending, name='investment_pending'),
    path('investment_approved/', views.investment_approved, name='investment_approved'),
    path('investment_disapproved/', views.investment_disapproved, name='investment_disapproved'),

    path('generate/pdf/investment/<int:investment_id>/', views.generate_investmentpdf, name='generate_investmentpdf'),
    path('generate/pdf/investment/payment/<int:investmentpayment_id>/', views.generate_investmentpaymentpdf, name='generate_investmentpaymentpdf'),
    path('investment/pdf/view/', views.render_investmentpdf_view, name='render_investmentpdf_view'),

    path('view/investment/interest/', views.view_investmentinterest, name='view_investmentinterest'),
    path('add/investment/interest/', views.add_investmentinterest, name='add_investmentinterest'),
    path('update/investment/interest/<slug:slug>/', views.update_investmentinterest, name='update_investmentinterest'),
    path('delete/investment/interest/<slug:slug>/', views.delete_investmentinterest, name='delete_investmentinterest'),

    path('view/investment/duration/', views.view_investmentduration, name='view_investmentduration'),
    path('add/investment/duration/', views.add_investmentduration, name='add_investmentduration'),
    path('update/investment/duration/<slug:slug>/', views.update_investmentduration, name='update_investmentduration'),
    path('delete/investment/duration/<slug:slug>/', views.delete_investmentduration, name='delete_investmentduration'),

    path('add/superuser/', views.add_superuser, name='add_superuser'),
    path('view/superuser/', views.view_superuser, name='view_superuser'),
    path('update/superuser/<int:pk>/', views.update_superuser, name='update_superuser'),
    path('delete/superuser/<int:pk>/', views.delete_superuser, name='delete_superuser'),

    path('add/user/', views.add_user, name='add_user'),
    path('view/user/', views.view_user, name='view_user'),
    path('update/user/<int:pk>/', views.update_user, name='update_user'),
    path('delete/user/<int:pk>/', views.delete_user, name='delete_user'),

    path('super/user/', views.super_user, name='super_user'),
    path('staff/user/', views.staff_user, name='staff_user'),
    path('regular/user/', views.regular_user, name='regular_user'),
    path('banned/user/', views.banned_user, name='banned_user'),

    path('edit/user/', views.edit_user, name='edit_user'),
    path('change/password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('view/profile/<str:username>/', views.view_profile, name='view_profile'),
    path('follow/', views.unfollow_or_follow, name='unfollow_or_follow'),
    
    path('view/post/', views.view_post, name='view_post'),
    path('add/post/', views.add_post, name='add_post'),
    path('update/post/<slug:slug>/', views.update_post, name='update_post'),
    path('delete/post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('author/post/', views.author_post, name='author_post'),
    path('view/approve/post/', views.view_approve_post, name='view_approve_post'),
    path('approve/post/view/', views.approve_post_view, name='approve_post_view'),
    path('disapprove/post/view/', views.disapprove_post_view, name='disapprove_post_view'),
    path('pending/post/view/', views.pending_post_view, name='pending_post_view'),
    path('approve/post/<slug:slug>/', views.approve_post, name='approve_post'),
    path('disapprove/post/<slug:slug>/', views.disapprove_post, name='disapprove_post'),

    path('view/tags/', views.view_tags, name='view_tags'),
    path('add/tags/', views.add_tags, name='add_tags'),
    path('update/tags/<slug:slug>/', views.update_tags, name='update_tags'),
    path('delete/tags/<slug:slug>/', views.delete_tags, name='delete_tags'),

    path('view/category/', views.view_category, name='view_category'),
    path('add/category/', views.add_category, name='add_category'),
    path('update/category/<slug:slug>/', views.update_category, name='update_category'),
    path('delete/category/<slug:slug>/', views.delete_category, name='delete_category'),
    
    path('view/comment/', views.view_comment, name='view_comment'),
    path('delete/comment/<int:pk>/', views.delete_comment, name='delete_comment'),

    path('view/reply/', views.view_reply, name='view_reply'),
    path('delete/reply/<int:pk>/', views.delete_reply, name='delete_reply'),

    path('view/newsletter/', views.view_newsletter, name='view_newsletter'),
    path('delete/newsletter/<slug:slug>/', views.delete_newsletter, name='delete_newsletter'),

    path('view/mail/', views.view_mail, name='view_mail'),
    path('add/mail/', views.add_mail, name='add_mail'),
    path('update/mail/<slug:slug>/', views.update_mail, name='update_mail'),
    path('delete/mail/<slug:slug>/', views.delete_mail, name='delete_mail'),

    path('view/contact/', views.view_contact, name='view_contact'),
    path('update/contact/<slug:slug>/', views.update_contact, name='update_contact'),
    path('delete/contact/<slug:slug>/', views.delete_contact, name='delete_contact'),

    path('view/contactdetail/', views.view_contactdetail, name='view_contactdetail'),
    path('add/contactdetail/', views.add_contactdetail, name='add_contactdetail'),
    path('update/contactdetail/<slug:slug>/', views.update_contactdetail, name='update_contactdetail'),
    path('delete/contactdetail/<slug:slug>/', views.delete_contactdetail, name='delete_contactdetail'),

    path('view/about/', views.view_about, name='view_about'),
    path('add/about/', views.add_about, name='add_about'),
    path('update/about/<slug:slug>/', views.update_about, name='update_about'),
    path('delete/about/<slug:slug>/', views.delete_about, name='delete_about'),

    path('view/title/', views.view_title, name='view_title'),
    path('add/title/', views.add_title, name='add_title'),
    path('update/title/<slug:slug>/', views.update_title, name='update_title'),
    path('delete/title/<slug:slug>/', views.delete_title, name='delete_title'),

    path('view/service/', views.view_service, name='view_service'),
    path('add/service/', views.add_service, name='add_service'),
    path('update/service/<slug:slug>/', views.update_service, name='update_service'),
    path('delete/service/<slug:slug>/', views.delete_service, name='delete_service'),

    path('view/purpose/', views.view_purpose, name='view_purpose'),
    path('add/purpose/', views.add_purpose, name='add_purpose'),
    path('update/purpose/<slug:slug>/', views.update_purpose, name='update_purpose'),
    path('delete/purpose/<slug:slug>/', views.delete_purpose, name='delete_purpose'),

    path('view/statement/', views.view_statement, name='view_statement'),
    path('add/statement/', views.add_statement, name='add_statement'),
    path('update/statement/<slug:slug>/', views.update_statement, name='update_statement'),
    path('delete/statement/<slug:slug>/', views.delete_statement, name='delete_statement'),

    path('view/career/', views.view_career, name='view_career'),
    path('add/career/', views.add_career, name='add_career'),
    path('update/career/<slug:slug>/', views.update_career, name='update_career'),
    path('delete/career/<slug:slug>/', views.delete_career, name='delete_career'),

    path('view/team/', views.view_team, name='view_team'),
    path('view/all/team/', views.view_allteam, name='view_allteam'),
    path('add/team/', views.add_team, name='add_team'),
    path('update/team/<slug:slug>/', views.update_team, name='update_team'),
    path('delete/team/<slug:slug>/', views.delete_team, name='delete_team'),

    path('view/testimony/', views.view_testimony, name='view_testimony'),
    path('add/testimony/', views.add_testimony, name='add_testimony'),
    path('update/testimony/<slug:slug>/', views.update_testimony, name='update_testimony'),
    path('delete/testimony/<slug:slug>/', views.delete_testimony, name='delete_testimony'),

    path('view/advert/', views.view_advert, name='view_advert'),
    path('add/advert/', views.add_advert, name='add_advert'),
    path('update/advert/<slug:slug>/', views.update_advert, name='update_advert'),
    path('delete/advert/<slug:slug>/', views.delete_advert, name='delete_advert'),

    path('view/occupation/', views.view_occupation, name='view_occupation'),
    path('add/occupation/', views.add_occupation, name='add_occupation'),
    path('update/occupation/<slug:slug>/', views.update_occupation, name='update_occupation'),
    path('delete/occupation/<slug:slug>/', views.delete_occupation, name='delete_occupation'),

   
    path('view/faq/', views.view_faq, name='view_faq'),
    path('add/faq/', views.add_faq, name='add_faq'),
    path('update/faq/<slug:slug>/', views.update_faq, name='update_faq'),
    path('delete/faq/<slug:slug>/', views.delete_faq, name='delete_faq'),

    path('view/event/', views.view_event, name='view_event'),
    path('add/event/', views.add_event, name='add_event'),
    path('update/event/<slug:slug>/', views.update_event, name='update_event'),
    path('delete/event/<slug:slug>/', views.delete_event, name='delete_event'),
   
    path('view/gallery/', views.view_gallery, name='view_gallery'),
    path('add/gallery/', views.add_gallery, name='add_gallery'),
    path('update/gallery/<slug:slug>/', views.update_gallery, name='update_gallery'),
    path('delete/gallery/<slug:slug>/', views.delete_gallery, name='delete_gallery'),

    path('view/header/', views.view_header, name='view_header'),
    path('add/header/', views.add_header, name='add_header'),
    path('update/header/<slug:slug>/', views.update_header, name='update_header'),
    path('delete/header/<slug:slug>/', views.delete_header, name='delete_header'),

    path('view/footer/', views.view_footer, name='view_footer'),
    path('add/footer/', views.add_footer, name='add_footer'),
    path('update/footer/<slug:slug>/', views.update_footer, name='update_footer'),
    path('delete/footer/<slug:slug>/', views.delete_footer, name='delete_footer'),
    
]