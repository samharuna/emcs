from django.urls import path
from applications import views

urlpatterns = [
     path('view/loan/', views.view_loan, name='view-loan'),
     path('add/loan/', views.add_loan, name='add-loan'),
     path('update/loan/<slug:slug>/', views.update_loan, name='update-loan'),
     path('delete/loan/<slug:slug>/', views.delete_loan, name='delete-loan'),
     
     path('edit/loan_status/<slug:slug>/', views.edit_loanstatus, name='edit-loanstatus'),
     path('payment/loan/<slug:slug>/', views.loan_payment, name='loan-payment'),
     path('applicant/loan/', views.applicant_loan, name='applicant-loan'),
     
     path('approve/loan/<slug:slug>/', views.approve_loan, name='approve-loan'),
     path('disapprove/loan/<slug:slug>/', views.disapprove_loan, name='disapprove-loan'),
     
     path('loan/pending/', views.loan_pending, name='loan-pending'),
     path('loan/approved/', views.loan_approved, name='loan-approved'),
     path('loan/disapproved/', views.loan_disapproved, name='loan-disapproved'),
     path('approve/loan/', views.approve_loan_view, name='approve-loanview'),
     
     path('generate/pdf_loan_application/<int:loan_id>/', views.generate_loanpdf, name='generate-loanpdf'),
     path('generate/pdf_loan_payment/<int:loanpayment_id>/', views.generate_loanpaymentpdf, name='generate-loanpaymentpdf'),
     path('loan/pdf_view/', views.render_loanpdf_view, name='render-loanpdf-view'),
     
     path('view/loan_duration/', views.view_loanduration, name='view-loanduration'),
     path('add/loan_duration/', views.add_loanduration, name='add-loanduration'),
     path('update/loan_duration/<slug:slug>/', views.update_loanduration, name='update-loanduration'),
     path('delete/loan_duration/<slug:slug>/', views.delete_loanduration, name='delete-loanduration'),
     
     path('applicant/passport/', views.applicant_passport, name='applicant-passport'),
     
     path('view/investment/', views.view_investment, name='view-investment'),
     path('add/investment/', views.add_investment, name='add-investment'),
     path('update/investment/<slug:slug>/', views.update_investment, name='update-investment'),
     path('delete/investment/<slug:slug>/', views.delete_investment, name='delete-investment'),
     
     path('edit/investment_status/<slug:slug>/', views.edit_investmentstatus, name='edit-investmentstatus'),
     path('payment/investment/<slug:slug>/', views.investment_payment, name='investment-payment'),
     path('investor/investment/', views.investor_investment, name='investor-investment'),
     
     path('approve/investment/<slug:slug>/', views.approve_investment, name='approve-investment'),
     path('disapprove/investment/<slug:slug>/', views.disapprove_investment, name='disapprove-investment'),
     
     path('investment_pending/', views.investment_pending, name='investment-pending'),
     path('investment_approved/', views.investment_approved, name='investment-approved'),
     path('investment_disapproved/', views.investment_disapproved, name='investment-disapproved'),
     path('approve/investment_view/', views.approve_investment_view, name='approve-investmentview'),

     path('generate/pdf_investment/<int:investment_id>/', views.generate_investmentpdf, name='generate-investmentpdf'),
     path('generate/pdf_investment_payment/<int:investmentpayment_id>/', views.generate_investmentpaymentpdf, name='generate-investmentpaymentpdf'),
     path('investment/pdf_view/', views.render_investmentpdf_view, name='render-investmentpdf-view'),

     path('view/investment_duration/', views.view_investmentduration, name='view-investmentduration'),
     path('add/investment_duration/', views.add_investmentduration, name='add-investmentduration'),
     path('update/investment_duration/<slug:slug>/', views.update_investmentduration, name='update-investmentduration'),
     path('delete/investment_duration/<slug:slug>/', views.delete_investmentduration, name='delete-investmentduration'),
     
     path('investor/passport/', views.investor_passport, name='investor-passport'),
     
     path('view/requirement/', views.view_requirement, name='view-requirement'),
     path('add/requirement/', views.add_requirement, name='add-requirement'),
     path('update/requirement/<slug:slug>/', views.update_requirement, name='update-requirement'),
     path('delete/requirement/<slug:slug>/', views.delete_requirement, name='delete-requirement'),
]
