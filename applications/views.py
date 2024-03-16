from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from xhtml2pdf import pisa
from applications.models import Loan, LoanDuration, Investment, InvestmentDuration, Requirement
from applications.forms import LoanForm, LoanDurationForm,  UpdateLoanForm, LoanPaymentForm, InvestmentForm, UpdateInvestmentForm, InvestmentPaymentForm, InvestmentDurationForm, RequirementForm
from backend.forms import ProfileForm, ProfilePictureForm, UpdateUserForm
from backend.decorators import allowed_users


# START OF LOAN
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_loan(request):
    loan = Loan.objects.all().order_by('-id')
    context = {'key':'Loan Application', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()
               }
    return render(request, 'applications/service/loan/view_loan.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def add_loan(request):    
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = UpdateUserForm(request.POST or None, instance=request.user)
        form = LoanForm(request.POST or None, request.FILES or None)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            messages.success(request, 'Your loan application submission was successful')
            return redirect('applicant-loan')
        else:
            messages.warning(request, 'Loan Application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = UpdateUserForm(instance=request.user)
        form = LoanForm()
    context = {'key':'Loan Application', 'form':form, 
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count(),
               'p_form':p_form, 'u_form':u_form}
    return render(request, 'applications/service/loan/add_loan.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def update_loan(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = UpdateUserForm(request.POST or None, instance=request.user)
        form = LoanForm(request.POST or None, request.FILES or None, instance=loan)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            form.save()
            messages.success(request, 'Your loan application submission was successful')
            return redirect('applicant-loan')
        else:
            messages.warning(request, 'Your loan application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = UpdateUserForm(instance=request.user)
        form = LoanForm(instance=loan)
    context = {'key':'Loan Application', 'form':form, 
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count(),
               'p_form':p_form, 'u_form':u_form}
    return render(request, 'applications/service/loan/update_loan.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_loan(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        loan.delete()
        messages.success(request, 'The Loan Application was deleted successfully')
        return redirect('approve-loanview')
    context = {'key':'Loan Application', 'item':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/service/loan/delete_loan.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def applicant_loan(request):
    loan = Loan.objects.filter(applicant=request.user).order_by('-date_created')
    context = {'key':'Applicant Loan Applied', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/applicant/loan_applicant.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def approve_loan_view(request):
    loan = Loan.objects.all().order_by('-id')
    context = {'key':'Approve Loan Application', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/loan/loan_approve_view.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def approve_loan(request, slug):
    approve = get_object_or_404(Loan, slug=slug)
    approve.status = 1
    approve.save()
    messages.success(request, 'Your loan application with Empower Multipurpose Cooperative Society was approved successfully')
    return redirect('approve-loanview')

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def disapprove_loan(request, slug):
    disapprove = get_object_or_404(Loan, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.info(request, 'Your loan application with Empower Multipurpose Cooperative Society was not approve')
    return redirect('approve-loanview')

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def loan_pending(request):
    loan = Loan.objects.filter(status=0)
    context = {'key':'Loan Pending', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/loan/loan_pending.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def loan_approved(request):
    loan = Loan.objects.filter(status=1)
    context = {'key':'Loan Approved', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/loan/loan_approved.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def loan_disapproved(request):
    loan = Loan.objects.filter(status=2)
    context = {'key':'Loan Disapproved', 'loan':loan,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/loan/loan_disapproved.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_loanstatus(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        form = UpdateLoanForm(request.POST or None,  instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Application Status Update was successful')
            return redirect('approve-loanview')
        else:
            messages.warning(request, 'Loan Application Status Update was not successful')
    else:
        form = UpdateLoanForm(instance=loan)
    context = {'key':'Loan Application', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/loan/edit_loan_status.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def loan_payment(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        form = LoanPaymentForm(request.POST or None, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Payment Plan Submission was successful')
            return redirect('approve-loanview')
        else:
            messages.warning(request, 'Loan Payment Plan Submission was not successful')
    else:
        form = LoanPaymentForm(instance=loan)
    context = {'key':'Loan Payment Plan', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/payment/loan/loan_payment_details.html', context)
# END OF LOAN

# START OF LOAN DURATION
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def view_loanduration(request):
    duration = LoanDuration.objects.all()
    context = {'key':'Loan Duration', 'duration':duration,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/loan/loanduration_view.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def add_loanduration(request):
    if request.method == "POST":
        form = LoanDurationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Duration addition was Successful')
            return redirect('view-loanduration')
        else:
            messages.warning(request, 'Loan Duration addition was not Successful')
    else:
        form = LoanDurationForm()
    context = {'key':'Loan Duration', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/loan/loanduration_add.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def update_loanduration(request, slug):
    duration = get_object_or_404(LoanDuration, slug=slug)
    if request.method == "POST":
        form = LoanDurationForm(request.POST or None, instance=duration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Duration update was Successful')
            return redirect('view-loanduration')
        else:
            messages.warning(request, 'Loan Duration update was not Successful')
    else:
        form = LoanDurationForm(instance=duration)
    context = {'key':'Update Loan Duration', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/loan/loanduration_update.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_loanduration(request, slug):
    duration = get_object_or_404(LoanDuration, slug=slug)
    if request.method == "POST":
        duration.delete()
        messages.success(request, 'Loan Duration was deleted Successfully')
        return redirect('view-loanduration')
    context = {'key':'Delete Loan Duration', 'item':duration,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()
               }
    return render(request, 'applications/duration/loan/loanduration_delete.html', context)
#  END OF LOAN DURATION

# START OF RENDER TO PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
# END OF RENDER TO PDF

# START OF GENERATE LOAN PDF 
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_loanpdf(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    pdf = render_to_pdf('applications/payment/loan/loan.html', {'loan':loan, 'key':'Generated PDF for Loan'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Loan Application Form for %s.pdf" %loan.applicant.get_full_name()
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE LOAN PDF 

# START OF GENERATE LOAN INVOICE PDF 
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_loanpaymentpdf(request, loanpayment_id):
    loan = get_object_or_404(Loan, pk=loanpayment_id)
    pdf = render_to_pdf('applications/payment/loan/loan_payment.html', {'loan':loan, 'key':'Generated PDF for Loan Payment Advice'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Loan Repayment Analysis for %s.pdf" %loan.applicant.get_full_name()
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE LOAN INVOICE PDF 

# TO VIEW PDF LOAN
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def render_loanpdf_view(request):
    loan = Loan.objects.filter(status=1)
    
    loan_principal = Loan.objects.filter(status=1).aggregate(sum=Sum('amount'))
    loan_interest  = Loan.objects.filter(status=1).annotate(get_interest=ExpressionWrapper(F('percent') * F('amount') / 100, output_field=IntegerField())).aggregate(sum=Sum('get_interest'))
    loan_repayment = Loan.objects.filter(status=1).annotate(get_total_amount=ExpressionWrapper(F('percent') * F('amount') /100 + F('amount'), output_field=IntegerField())).aggregate(sum=Sum('get_total_amount'))

    template_path = 'applications/payment/loan/loan_invoice.html'
    context = {'loan': loan, 'loan_principal':loan_principal, 'loan_repayment':loan_repayment, 'loan_interest': loan_interest, 
               'key':'Loan Granted Analysis'
               }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Loan Granted Analysis.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
# TO VIEW PDF LOAN


# START OF UPLOAD PASSPORT FOR LOAN
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def applicant_passport(request):
    if request.method == "POST":
        applicant_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if applicant_form.is_valid():
            applicant_form.save()
        return redirect('add-loan')
    else:
        applicant_form = ProfilePictureForm(instance=request.user.profile)
        
# END OF UPLOAD PASSPORT FOR LOAN


# START of INVESTMENT
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_investment(request):
    investment = Investment.objects.all().order_by('-id')
    context = {'key':'Investment', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/service/investment/view_investment.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def add_investment(request):
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = UpdateUserForm(request.POST or None, instance=request.user)
        form = InvestmentForm(request.POST or None, request.FILES or None)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            instance = form.save(commit=False)
            instance.investor = request.user
            instance.save()
            messages.success(request, 'Your investment application submission was successful')
            return redirect('investor-investment')
        else:
            messages.warning(request, 'Your investment application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = UpdateUserForm(instance=request.user)
        form = InvestmentForm()
    context = {'key':'Add Investment', 'form':form, 'p_form':p_form, 'u_form':u_form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/service/investment/add_investment.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def update_investment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = UpdateUserForm(request.POST or None, instance=request.user)
        form = InvestmentForm(request.POST or None, request.FILES or None, instance=investment)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            form.save()
            messages.success(request, 'Your investment application submission was successful')
            return redirect('investor-investment')
        else:
            messages.warning(request, 'Your investment application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = UpdateUserForm(instance=request.user)
        form = InvestmentForm(instance=investment)
    context = {'key':'Investment', 'form':form, 'p_form':p_form, 'u_form':u_form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/service/investment/update_investment.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_investment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        investment.delete()
        messages.success(request, 'The Investment Application was deleted successfully')
        return redirect('approve-investmentview')
    context = {'key':'Investment', 'item':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/service/investment/delete_investment.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def investor_investment(request):
    investment = Investment.objects.filter(investor=request.user)
    context = {'key':'Investor', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/investor/investment_investor.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def approve_investment_view(request):
    investment = Investment.objects.all()
    context = {'key':'Approve Investment', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/investment/investment_approve_view.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def approve_investment(request, slug):
    approve = get_object_or_404(Investment, slug=slug)
    approve.status = 1
    approve.save()
    messages.success(request, 'Your investment application with EMCS was approved successfully')
    return redirect('approve-investmentview')

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def disapprove_investment(request, slug):
    disapprove = get_object_or_404(Investment, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.info(request, 'Your investment application with EMCS was not approve')
    return redirect('approve-investmentview')

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def investment_pending(request):
    investment = Investment.objects.filter(status=0)
    context = {'key':'Investment Pending', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/investment/investment_pending.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def investment_approved(request):
    investment = Investment.objects.filter(status=1)
    context = {'key':'Investment Approved', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/investment/investment_approved.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def investment_disapproved(request):
    investment = Investment.objects.filter(status=2)
    context = {'key':'Investment Disapproved', 'investment':investment,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/investment/investment_disapproved.html', context)
# START of INVESTMENT

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_investmentstatus(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        form = UpdateInvestmentForm(request.POST or None,  instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Application Status Update was successful')
            return redirect('approve-investmentview')
        else:
            messages.warning(request, 'Investment Application Status Update was not successful')
    else:
        form = UpdateInvestmentForm(instance=investment)
    context = {'key':'Investment Application', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/admin/investment/edit_investment_status.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def investment_payment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        form = InvestmentPaymentForm(request.POST or None, instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Details Submission was successful')
            return redirect('approve-investmentview')
        else:
            messages.warning(request, 'Investment Details Submission was not successful')
    else:
        form = InvestmentPaymentForm(instance=investment)
    context = {'key':'Investment Payment Plan', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/payment/investment/investment_payment_details.html', context)

# START OF INVESTMENT DURATION
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def view_investmentduration(request):
    duration = InvestmentDuration.objects.all()
    context = {'key':'Investment Duration', 'duration':duration,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/investment/investmentduration_view.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def add_investmentduration(request):
    if request.method == "POST":
        form = InvestmentDurationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Duration addition was Successful')
            return redirect('view-investmentduration')
        else:
            messages.warning(request, 'Investment Duration addition was not Successful')
    else:
        form = InvestmentDurationForm()
    context = {'key':'Investment Duration', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/investment/investmentduration_add.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def update_investmentduration(request, slug):
    duration = get_object_or_404(InvestmentDuration, slug=slug)
    if request.method == "POST":
        form = InvestmentDurationForm(request.POST or None, instance=duration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Duration update was Successful')
            return redirect('view-investmentduration')
        else:
            messages.info(request, 'Investment Duration update was not Successful')
    else:
        form = InvestmentDurationForm(instance=duration)
    context = {'key':'Update Investment Duration', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/investment/investmentduration_update.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_investmentduration(request, slug):
    duration = get_object_or_404(InvestmentDuration, slug=slug)
    if request.method == "POST":
        duration.delete()
        messages.success(request, 'Investment Duration was deleted Successfully')
        return redirect('view-investmentduration')
    context = {'key':'Delete Investment Duration', 'item':duration,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/duration/investment/investmentduration_delete.html', context)
#  END OF INVESTMENT DURATION

# START OF GENERATE INVESTMENT PDF 
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_investmentpdf(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    pdf = render_to_pdf('applications/payment/investment/investment.html', {'investment':investment, 'key':'Generated PDF for Investment'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Investment Acknowledgement for %s.pdf" %investment.investor.get_full_name()
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE INVESTMENT PDF 

# START OF GENERATE INVESTMENT INVOICE PDF 
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_investmentpaymentpdf(request, investmentpayment_id):
    investment = get_object_or_404(Investment, pk=investmentpayment_id)
    pdf = render_to_pdf('applications/payment/investment/investment_payment.html', {'investment':investment, 'key':'Generated PDF for Investment Payment Advice'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Investment Payment Advice for %s.pdf" %investment.investor.get_full_name()
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE INVESTMENT INVOICE PDF 

# TO VIEW PDF INVESTMENT
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def render_investmentpdf_view(request):
    investment = Investment.objects.filter(status=1)
    
    investment_principal    = Investment.objects.filter(status=1).aggregate(sum=Sum('amount'))
    investment_interest     = Investment.objects.filter(status=1).annotate(get_investment_interest=ExpressionWrapper(F('percent') * F('amount') / 100 / 2, output_field=IntegerField())).aggregate(sum=Sum('get_investment_interest'))
    investment_repayment    = Investment.objects.filter(status=1).annotate(get_total_investment=ExpressionWrapper(F('percent') * F('amount') /100 / 2 + F('amount'),output_field=IntegerField())).aggregate(sum=Sum('get_total_investment'))
    
    template_path = 'applications/payment/investment/investment_invoice.html'
    context = {'investment': investment, 'investment_principal':investment_principal, 'investment_interest':investment_interest,
               'investment_repayment':investment_repayment, 'key':'Investment Analysis'}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Investment Analysis.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
# TO VIEW PDF INVESTMENT

# START OF UPLOAD PASSPORT FOR INVESTMENT
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def investor_passport(request):
    if request.method == "POST":
        investor_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if investor_form.is_valid():
            investor_form.save()
        return redirect('add-investment')
    else:
        investor_form = ProfilePictureForm(instance=request.user.profile)
# END OF UPLOAD PASSPORT FOR INVESTMENT

# START OF SERVICES REQUIREMENT
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def view_requirement(request):
    requirement = Requirement.objects.all()
    context = {'key':'View Requirement', 'requirement':requirement,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/requirement/view_requirement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def add_requirement(request):
    if request.method == "POST":
        form = RequirementForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Requirement addition was Successful')
            return redirect('view-requirement')
        else:
            messages.warning(request, 'Service Requirement addition was not Successful')
    else:
        form = RequirementForm()
    context = {'key':'Add Requirement', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/requirement/add_requirement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def update_requirement(request, slug):
    requirement = get_object_or_404(Requirement, slug=slug)
    if request.method == "POST":
        form = RequirementForm(request.POST or None, instance=requirement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service requirement update was Successful')
            return redirect('view-requirement')
        else:
            messages.info(request, 'Service requirement update was not Successful')
    else:
        form = RequirementForm(instance=requirement)
    context = {'key':'Update Requirement', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/requirement/update_requirement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_requirement(request, slug):
    requirement = get_object_or_404(Requirement, slug=slug)
    if request.method == "POST":
        requirement.delete()
        messages.success(request, 'Service Requirement was deleted Successfully')
        return redirect('view-requirement')
    context = {'key':'Delete Requirement', 'requirement':requirement,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'applications/requirement/delete_requirement.html', context)
#  END OF SERVICES REQUIREMENT

