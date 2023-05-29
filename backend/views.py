from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django_pandas.io import read_frame
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import Group
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from xhtml2pdf import pisa
from accounts.models import User
from backend.models import Profile, Follow
from backend.forms import AddSuperUserForm, UpdateSuperUserForm, AddUserForm, UpdateUserForm, EditUserForm, ProfileForm, UserForm
from django.contrib.auth import update_session_auth_hash
from accounts.forms import ChangePasswordForm
from frontend.models import HeaderLogo, FooterLogo, Loan, LoanDuration, LoanInterest, Investment, InvestmentDuration, InvestmentInterest, Post, Tags, Category, Comment, Reply, About, Title, Occupation, Service, Purpose, Statement, Team, Testimony, Newsletter, Mail, Career, Advert, Contact, ContactDetail, Faq, Event, Gallery
from frontend.forms import HeaderLogoForm, FooterLogoForm, LoanForm, LoanDurationForm, LoanInterestForm, UpdateLoanForm, LoanPaymentForm, InvestmentForm, UpdateInvestmentForm, InvestmentPaymentForm, InvestmentDurationForm, InvestmentInterestForm, PostForm, TagsForm, OccupationForm, CategoryForm, CommentForm, ReplyForm, AboutForm, TitleForm, ServiceForm, PurposeForm, StatementForm, TeamForm, TestimonyForm, NewsletterForm, MailForm, CareerForm, AdvertForm, ContactForm, ContactDetailForm, FaqForm, EventForm, GalleryForm
from backend.decorators import allowed_users


# Create your views here.
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def dashboard(request):
    loan                    = Loan.objects.all().order_by('-id')
    applicant_loan          = Loan.objects.filter(applicant=request.user).order_by('-id')
    applicant_investment    = Investment.objects.filter(investor=request.user).order_by('-id')
    context = {'key':'Dashboard', 'loan':loan, 'applicant_loan':applicant_loan, 'applicant_investment':applicant_investment}

    return render(request, 'backend/index.html', context)

# START OF LOAN
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_loan(request):
    loan = Loan.objects.all().order_by('-id')
    context = {'key':'Loan Application', 'loan':loan}
    return render(request, 'application/loan_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def add_loan(request):
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = EditUserForm(request.POST or None, instance=request.user)
        form = LoanForm(request.POST or None, request.FILES or None)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            messages.success(request, 'Your loan application submission was successful')
            return redirect('applicant_loan')
        else:
            messages.info(request, 'Loan Application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = EditUserForm(instance=request.user)
        form = LoanForm()
    context = {'key':'Loan Application', 'form':form, 'p_form':p_form, 'u_form':u_form}
    return render(request, 'application/loan_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def update_loan(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = EditUserForm(request.POST or None, instance=request.user)
        form = LoanForm(request.POST or None, request.FILES or None, instance=loan)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            form.save()
            messages.success(request, 'Your loan application submission was successful')
            return redirect('applicant_loan')
        else:
            messages.info(request, 'Your loan application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = EditUserForm(instance=request.user)
        form = LoanForm(instance=loan)
    context = {'key':'Loan Application', 'form':form, 'p_form':p_form, 'u_form':u_form}
    return render(request, 'application/loan_update.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def edit_loan(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        form = UpdateLoanForm(request.POST or None,  instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Application Status Update was successful')
            return redirect('approve_loan_view')
        else:
            messages.info(request, 'Loan Application Status Update was not successful')
    else:
        form = UpdateLoanForm(instance=loan)
    context = {'key':'Loan Application', 'form':form}
    return render(request, 'application/loan_edit.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def loan_payment(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        form = LoanPaymentForm(request.POST or None, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Payment Plan Submission was successful')
            return redirect('approve_loan_view')
        else:
            messages.info(request, 'Loan Payment Plan Submission was not successful')
    else:
        form = LoanPaymentForm(instance=loan)
    context = {'key':'Loan Payment Plan', 'form':form}
    return render(request, 'application/loan_payment.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_loan(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    if request.method == "POST":
        loan.delete()
        messages.success(request, 'The Loan Application was deleted successfully')
        return redirect('approve_loan_view')
    context = {'key':'Loan Application', 'item':loan}
    return render(request, 'application/loan_delete.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def applicant_loan(request):
    loan = Loan.objects.filter(applicant=request.user).order_by('-date_created')
    context = {'key':'Applicant Loan Applied', 'loan':loan}
    return render(request, 'application/loan_applicant.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def approve_loan_view(request):
    loan = Loan.objects.all().order_by('-id')
    context = {'key':'Approve Loan Application', 'loan':loan}
    return render(request, 'application/loan_approve_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def approve_loan(request, slug):
    approve = get_object_or_404(Loan, slug=slug)
    approve.status = 1
    approve.save()
    messages.success(request, 'Your loan application with EMCS was approved successfully')
    return redirect('approve_loan_view')

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def disapprove_loan(request, slug):
    disapprove = get_object_or_404(Loan, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.info(request, 'Your loan application with EMCS was not approve')
    return redirect('approve_loan_view')

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def loan_pending(request):
    loan = Loan.objects.filter(status=0)
    context = {'key':'Loan Pending', 'loan':loan}
    return render(request, 'application/loan_pending.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def loan_approved(request):
    loan = Loan.objects.filter(status=1)
    context = {'key':'Loan Approved', 'loan':loan}
    return render(request, 'application/loan_approved.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def loan_disapproved(request):
    loan = Loan.objects.filter(status=2)
    context = {'key':'Loan Disapproved', 'loan':loan}
    return render(request, 'application/loan_disapproved.html', context)
# END OF LOAN


# START of INVESTMENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_investment(request):
    investment = Investment.objects.all().order_by('-id')
    context = {'key':'Investment', 'investment':investment}
    return render(request, 'application/investment_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def add_investment(request):
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = EditUserForm(request.POST or None, instance=request.user)
        form = InvestmentForm(request.POST or None, request.FILES or None)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            instance = form.save(commit=False)
            instance.investor = request.user
            instance.save()
            messages.success(request, 'Your investment application submission was successful')
            return redirect('investor_investment')
        else:
            messages.info(request, 'Your investment application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = EditUserForm(instance=request.user)
        form = InvestmentForm()
    context = {'key':'Add Investment', 'form':form, 'p_form':p_form, 'u_form':u_form}
    return render(request, 'application/investment_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def update_investment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        p_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        u_form = EditUserForm(request.POST or None, instance=request.user)
        form = InvestmentForm(request.POST or None, request.FILES or None, instance=investment)
        if p_form.is_valid() and u_form.is_valid() and form.is_valid():
            p_form.save()
            u_form.save()
            form.save()
            messages.success(request, 'Your investment application submission was successful')
            return redirect('investor_investment')
        else:
            messages.info(request, 'Your investment application submission was not successful')
    else:
        p_form = ProfileForm(instance=request.user.profile)
        u_form = EditUserForm(instance=request.user)
        form = InvestmentForm(instance=investment)
    context = {'key':'Investment', 'form':form, 'p_form':p_form, 'u_form':u_form}
    return render(request, 'application/investment_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def edit_investment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        form = UpdateInvestmentForm(request.POST or None,  instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Application Status Update was successful')
            return redirect('approve_investment_view')
        else:
            messages.info(request, 'Investment Application Status Update was not successful')
    else:
        form = UpdateInvestmentForm(instance=investment)
    context = {'key':'Investment Application', 'form':form}
    return render(request, 'application/investment_edit.html', context)


@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def investment_payment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        form = InvestmentPaymentForm(request.POST or None, instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Details Submission was successful')
            return redirect('approve_investment_view')
        else:
            messages.info(request, 'Investment Details Submission was not successful')
    else:
        form = InvestmentPaymentForm(instance=investment)
    context = {'key':'Investment Payment Plan', 'form':form}
    return render(request, 'application/investment_payment.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_investment(request, slug):
    investment = get_object_or_404(Investment, slug=slug)
    if request.method == "POST":
        investment.delete()
        messages.success(request, 'The Investment Application was deleted successfully')
        return redirect('approve_investment_view')
    context = {'key':'Investment', 'item':investment}
    return render(request, 'application/investment_delete.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "customer"])
def investor_investment(request):
    investment = Investment.objects.filter(investor=request.user)
    context = {'key':'Investor', 'investment':investment}
    return render(request, 'application/investment_investor.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def approve_investment_view(request):
    investment = Investment.objects.all()
    context = {'key':'Approve Investment', 'investment':investment}
    return render(request, 'application/investment_approve_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def approve_investment(request, slug):
    approve = get_object_or_404(Investment, slug=slug)
    approve.status = 1
    approve.save()
    messages.success(request, 'Your investment application with EMCS was approved successfully')
    return redirect('approve_investment_view')

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def disapprove_investment(request, slug):
    disapprove = get_object_or_404(Investment, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.info(request, 'Your investment application with EMCS was not approve')
    return redirect('approve_investment_view')

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def investment_pending(request):
    investment = Investment.objects.filter(status=0)
    context = {'key':'Investment Pending', 'investment':investment}
    return render(request, 'application/investment_pending.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def investment_approved(request):
    investment = Investment.objects.filter(status=1)
    context = {'key':'Investment Approved', 'investment':investment}
    return render(request, 'application/investment_approved.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def investment_disapproved(request):
    investment = Investment.objects.filter(status=2)
    context = {'key':'Investment Disapproved', 'investment':investment}
    return render(request, 'application/investment_disapproved.html', context)
# START of INVESTMENT


# Super USER
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def add_superuser(request):
    if request.method == "POST":
        form = AddSuperUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account creation for {username} was successful')

            group = Group.objects.get(name="admin")
            user.groups.add(group)
            
            return redirect('view_superuser')
        else:
            messages.info(request, f'The account creation was not successful')
    else:
        form = AddSuperUserForm()
    context = {'key':'Add Super User', 'form':form}
    return render(request, 'profiles/superuser_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def update_superuser(request, pk):
    accounts = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = UpdateSuperUserForm(request.POST or None, instance=accounts)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Account update for '{username}' was successful")
            return redirect('view_superuser')
        else:
            messages.info(request, 'Account update was not successful')
    else:
        form = UpdateSuperUserForm(instance=accounts)
    context = {'key':'Update Super User', 'form':form}
    return render(request, 'profiles/superuser_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_superuser(request, pk):
    accounts = get_object_or_404(User, id=pk)
    if request.method == "POST":
        accounts.delete()
        messages.success(request, 'The user account was deleted successfully')
        return redirect('view_superuser')
    context = {'key':'Delete Super User', 'item':accounts}
    return render(request, 'profiles/superuser_delete.html', context)
    
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def view_superuser(request):
    accounts = User.objects.filter(is_superuser=True)
    context = {'key':'View Super User', 'accounts':accounts}
    return render(request, 'profiles/superuser_view.html', context)

# END Super USER


# START OF USER
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account creation for {username} was successful')

            group = Group.objects.get(name="staff")
            user.groups.add(group)
            
            return redirect('view_user')
        else:
            messages.info(request, f'The account creation was not successful')
    else:
        form = AddUserForm()
    context = {'key':'Add User', 'form':form}
    return render(request, 'profiles/user_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_user(request, pk):
    accounts = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = UpdateUserForm(request.POST or None, instance=accounts)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Account update for '{username}' was successful")
            return redirect('view_user')
        else:
            messages.info(request, 'Account update was not successful')
    else:
        form = UpdateUserForm(instance=accounts)
    context = {'key':'Update User', 'form':form}
    return render(request, 'profiles/user_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_user(request, pk):
    accounts = get_object_or_404(User, id=pk)
    if request.method == "POST":
        accounts.delete()
        messages.success(request, 'The user account was deleted successfully')
        return redirect('view_user')
    context = {'key':'Delete User', 'item':accounts}
    return render(request, 'profiles/user_delete.html', context)
    
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_user(request):
    accounts = User.objects.all()
    context = {'key':'View User', 'accounts':accounts}
    return render(request, 'profiles/user_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request, f'Account update for {user} was successful')
            return redirect('edit_user')
        else:
            messages.info(request, 'Your account update was not successful')
    else:
        form = UserForm(instance=user)
    context = {'key':'Edit User', 'form':form}
    return render(request, 'profiles/user_edit.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password change was successful')
            return redirect('change_password')
        else:
            messages.info(request, 'Your password change was not successful')
    else:
        form = ChangePasswordForm(request.user)
    context = {'key':'Change Password', 'form':form}
    return render(request, 'profiles/change_password.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def profile(request):
    accounts = get_object_or_404(User, id=request.user.id)

    author = Post.objects.filter(author=request.user)
    author_count = author.count()

    if request.method == "POST":
        form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account profile update was successful')
            return redirect('profile')
        else:
            messages.info(request, 'Your account profile update was not successful')
    else:
        form = ProfileForm(instance=request.user.profile)
        
    context = {'key':'User Profile', 'accounts':accounts, 'form':form, 'author':author, 'author_count':author_count}
    return render(request, 'profiles/profile.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def view_profile(request, username):
    accounts = get_object_or_404(User, username=username)
    author = Post.objects.filter(author=request.user)
    
    current_user = get_object_or_404(User, username=username)
    logged_in_user = request.user.username

    followed_count = len(Follow.objects.filter(followed=current_user))
    followed_by_count = len(Follow.objects.filter(followed_by=current_user))

    author_follower = Follow.objects.filter(followed=current_user)

    followers = Follow.objects.filter(followed=current_user)
    data = []

    for key in followers:
        followers = key.followed_by
        data.append(followers)
    
    if logged_in_user in data:
        following = "unfollow"
    else:
        following = "follow"
    
    context = {'key': 'User Profile', 'accounts': accounts, 'author_follower':author_follower, 'author':author, 'following':following, 'current_user':current_user, 'followed_count':followed_count, 'followed_by_count':followed_by_count}
    return render(request, 'profiles/profile_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def unfollow_or_follow(request):
    if request.method == "POST":
        followed    = request.POST['followed']
        followed_by = request.POST['followed_by']
        value       = request.POST['value']

        if value == "follow":
            follows = Follow.objects.create(followed=followed, followed_by=followed_by)
            follows.save()
        else:
            follows = Follow.objects.get(followed=followed, followed_by=followed_by)
            follows.delete()

        return redirect(reverse('view_profile', kwargs={'username':followed}))

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def super_user(request):
    superuser = User.objects.filter(is_superuser=True)
    context = {'key':'Super User', 'superuser':superuser}
    return render(request, 'profiles/user_super.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def staff_user(request):
    staffuser = User.objects.filter(is_staff=True).exclude(is_superuser=True, is_active=True)
    context = {'key':'Staff User', 'staffuser':staffuser}
    return render(request, 'profiles/user_staff.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def regular_user(request):
    activeuser = User.objects.filter(is_active=True).exclude(is_superuser=True).exclude(is_staff=True)
    context = {'key':'Active User', 'activeuser':activeuser}
    return render(request, 'profiles/user_active.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def banned_user(request):
    banneduser = User.objects.filter(is_active=False)
    context = {'key':'Banned Users', 'banneduser':banneduser}
    return render(request, 'profiles/user_banned.html', context)
# END OF USER


# START OF POST
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def view_post(request):
    post = Post.objects.all()
    context = {'key':'View Post', 'post': post}
    return render(request, 'backend/post_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'Post addition was successful')
            return redirect('author_post')
        else:
            messages.info(request, 'Post addition was not successful')
    else:
        form = PostForm()
    context = {'key':'Add Post', 'form': form}
    return render(request, 'backend/post_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was successful')
            return redirect('author_post')
        else:
            messages.info(request, 'Post update was not successful')
    else:
        form = PostForm(instance=post)
    context = {'key':'Update Post', 'form': form}
    return render(request, 'backend/post_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Blog Post was deleted successfully')
        return redirect('view_post')
    context = {'key':'Delete Post', 'item':post}
    return render(request, 'backend/post_delete.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def author_post(request):
    post = Post.objects.filter(author=request.user)
    context = {'key': 'Author Posts', 'post':post}
    return render(request, 'backend/post_author.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_approve_post(request):
    post = Post.objects.all()
    context = {'key':'Approve Post', 'post':post}
    return render(request, 'backend/post_approve.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def approve_post_view(request):
    post = Post.objects.filter(status=1)
    context = {'key':'View Approve Post', 'post':post}
    return render(request, 'backend/post_approve_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def disapprove_post_view(request):
    post = Post.objects.filter(status=2)
    context = {'key':'View Disapprove Post', 'post':post}
    return render(request, 'backend/post_disapprove_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def pending_post_view(request):
    post = Post.objects.filter(status=0)
    context = {'key':'View Pending Post', 'post':post}
    return render(request, 'backend/post_pending_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def approve_post(request, slug):
    approve = get_object_or_404(Post, slug=slug)
    approve.status = 1
    approve.save()
    messages.info(request, 'Post approval was successful')
    return redirect('view_approve_post')

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def disapprove_post(request, slug):
    disapprove = get_object_or_404(Post, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.info(request, 'Post approval was not successful')
    return redirect('view_approve_post')
# END OF POST


# START OF TAGS
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_tags(request):
    tags = Tags.objects.all()
    context = {'key':'Tags', 'tags': tags}
    return render(request, 'backend/tags_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_tags(request):
    if request.method == "POST":
        form = TagsForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tags addition was successful')
            return redirect('view_tags')
        else:
            messages.info(request, 'Tags addition was not successful')
    else:
        form = TagsForm()
    context = {'key':'Add Tag', 'form': form}
    return render(request, 'backend/tags_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_tags(request, slug):
    tags = get_object_or_404(Tags, slug=slug)
    if request.method == "POST":
        form = TagsForm(request.POST or None, instance=tags)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tags post update was successful')
            return redirect('view_tags')
        else:
            messages.info(request, 'Tags post update was not successful')
    else:
        form = TagsForm(instance=tags)
    context = {'key':'Update Tag', 'form': form}
    return render(request, 'backend/tags_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_tags(request, slug):
    tags = get_object_or_404(Tags, slug=slug)
    if request.method == "POST":
        tags.delete()
        messages.success(request, 'Tags post was deleted Successfully')
        return redirect('view_tags')
    context = {'key':'Delete Tag', 'item':tags}
    return render(request, 'backend/tags_delete.html', context)
# END OF TAGS


# START OF CATEGORY
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_category(request):
    category = Category.objects.all()
    context = {'key':'Category', 'category':category}
    return render(request, 'backend/category_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category post addition was Successful')
            return redirect('view_category')
        else:
            messages.info(request, 'Category post addition was not Successful')
    else:
        form = CategoryForm()
    context = {'key':'Add Category', 'form': form}
    return render(request, 'backend/category_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form =CategoryForm(request.POST or None, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category post update was Successful')
            return redirect('view_category')
        else:
            messages.info(request, 'Category post update was not Successful')
    else:
        form =CategoryForm(instance=category)
    context = {'key':'Update Category', 'form': form}
    return render(request, 'backend/category_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        category.delete()
        messages.success(request, 'Category post was deleted Successfully')
        return redirect('view_category')
    context = {'key':'Delete Category', 'item':category}
    return render(request, 'backend/category_delete.html', context)
#  END OF CATEGORY

# START OF COMMENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_comment(request):
    comment = Comment.objects.all()
    context = {'key':'Comments', 'comment':comment}
    return render(request, 'backend/comment_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == "POST":
        comment.delete()
        messages.success(request, 'Comment post was deleted Successfully')
        return redirect('view_comment')
    context = {'key':'Delete Comment', 'item':comment}
    return render(request, 'backend/comment_delete.html', context)
#  END OF COMMENT

# START OF REPLY
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_reply(request):
    reply = Reply.objects.all()
    context = {'key':'Replies', 'reply':reply}
    return render(request, 'backend/reply_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    if request.method == "POST":
        reply.delete()
        messages.success(request, 'Reply post was deleted Successfully')
        return redirect('view_reply')
    context = {'key':'Delete Reply', 'item':reply}
    return render(request, 'backend/reply_delete.html', context)
#  END OF REPLY


# START OF NEWSLETTER
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_newsletter(request):
    newsletter = Newsletter.objects.all()
    context = {'key':'Newsletter', 'newsletter':newsletter}
    return render(request, 'backend/newsletter_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_newsletter(request, slug):
    newsletter = get_object_or_404(Newsletter, slug=slug)
    if request.method == "POST":
        newsletter.delete()
        messages.success(request, 'Newsletter post was deleted Successfully')
        return redirect('view_newsletter')
    context = {'key':'Delete Newsletter', 'item':newsletter}
    return render(request, 'backend/newsletter_delete.html', context)
#  END OF NEWSLETTER


# START OF SEND MAIL
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_mail(request):
    mail = Mail.objects.all()
    context = {'key':'Mail Sent', 'mail':mail}
    return render(request, 'backend/mail_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_mail(request):
    emails = Newsletter.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
 
    if request.method == "POST":
        form = MailForm(request.POST or None)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            send_mail(
                subject,
                body,
                '',
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Mail was sent Successfully')
            return redirect('view_mail')
        else:
            messages.info(request, 'Mail was not sent Successful')
    else:
        form = MailForm()
    context = {'key':'Send Mail', 'form': form}
    return render(request, 'backend/mail_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_mail(request, slug):
    emails = Newsletter.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    mail = get_object_or_404(Mail, slug=slug)
    if request.method == "POST":
        form = MailForm(request.POST or None, instance=mail)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            send_mail(
                subject,
                body,
                '',
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Mail was sent Successfully')
            return redirect('view_mail')
        else:
            messages.info(request, 'Mail was not not Successfully')
    else:
        form = MailForm(instance=mail)
    context = {'key':'Reply Mail', 'form': form}
    return render(request, 'backend/mail_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_mail(request, slug):
    mail = get_object_or_404(Mail, slug=slug)
    if request.method == "POST":
        mail.delete()
        messages.success(request, 'Mail post was deleted Successfully')
        return redirect('view_mail')
    context = {'key':'Delete Mail', 'item':mail}
    return render(request, 'backend/mail_delete.html', context)
#  END OF SEND MAIL


# START OF CONTACT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_contact(request):
    contact = Contact.objects.all().order_by("-id")
    context = {'key':'Contact', 'contact':contact}
    return render(request, 'backend/contact_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_contact(request, slug):
    contact = get_object_or_404(Contact, slug=slug)
    if request.method == "POST":
        form =ContactForm(request.POST or None, instance=contact)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            send_mail(
                subject,
                body,
                '',
                ['email'],
                fail_silently=False,
            )
            print(send_mail)
            messages.success(request, 'Message was sent Successful')
            return redirect('view_contact')
        else:
            messages.info(request, 'Message was not sent Successful')
    else:
        form =ContactForm(instance=contact)
    context = {'key':'Update Contact', 'form': form}
    return render(request, 'backend/contact_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_contact(request, slug):
    contact = get_object_or_404(Contact, slug=slug)
    if request.method == "POST":
        contact.delete()
        messages.success(request, 'Contact Message was deleted Successfully')
        return redirect('view_contact')
    context = {'key':'Delete Contact', 'item':contact}
    return render(request, 'backend/contact_delete.html', context)
#  END OF CONTACT


# START OF CONTACT DETAILS
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_contactdetail(request):
    contactdetail = ContactDetail.objects.all()
    context = {'key':'Contact Detail', 'contactdetail':contactdetail}
    return render(request, 'backend/contactdetail_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_contactdetail(request):
    if request.method == "POST":
        form = ContactDetailForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Detail post addition was Successful')
            return redirect('view_contactdetail')
        else:
            messages.info(request, 'Contact Detail post addition was not Successful')
    else:
        form = ContactDetailForm()
    context = {'key':'Add Contact Detail', 'form': form}
    return render(request, 'backend/contactdetail_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_contactdetail(request, slug):
    contactdetail = get_object_or_404(ContactDetail, slug=slug)
    if request.method == "POST":
        form = ContactDetailForm(request.POST or None, instance=contactdetail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Detail post update was Successful')
            return redirect('view_contactdetail')
        else:
            messages.info(request, 'Contact Detail post update was not Successful')
    else:
        form = ContactDetailForm(instance=contactdetail)
    context = {'key':'Update Contact Detail', 'form': form}
    return render(request, 'backend/contactdetail_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_contactdetail(request, slug):
    contactdetail = get_object_or_404(ContactDetail, slug=slug)
    if request.method == "POST":
        contactdetail.delete()
        messages.success(request, 'Contact Detail post was deleted Successfully')
        return redirect('view_contactdetail')
    context = {'key':'Delete Contact Detail', 'item':contactdetail}
    return render(request, 'backend/contactdetail_delete.html', context)
#  END OF CONTACT DETAILS


# START OF ABOUT US
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_about(request):
    about = About.objects.all()
    context = {'key':'About Page', 'about':about}
    return render(request, 'backend/about_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_about(request):
    if request.method == "POST":
        form = AboutForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'About post addition was Successful')
            return redirect('view_about')
        else:
            messages.info(request, 'About post addition was not Successful')
    else:
        form = AboutForm()
    context = {'key':'Add About', 'form': form}
    return render(request, 'backend/about_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_about(request, slug):
    about = get_object_or_404(About, slug=slug)
    if request.method == "POST":
        form = AboutForm(request.POST or None, request.FILES or None, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'About post update was Successful')
            return redirect('view_about')
        else:
            messages.info(request, 'About post update was not Successful')
    else:
        form = AboutForm(instance=about)
    context = {'key':'Update About', 'form': form}
    return render(request, 'backend/about_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_about(request, slug):
    about = get_object_or_404(About, slug=slug)
    if request.method == "POST":
        about.delete()
        messages.success(request, 'About post was deleted Successfully')
        return redirect('view_about')
    context = {'key':'Delete About', 'item':about}
    return render(request, 'backend/about_delete.html', context)
#  END OF ABOUT US


# START OF SERVICE TITLE
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_title(request):
    title = Title.objects.all()
    context = {'key':'Type of Service', 'title':title}
    return render(request, 'backend/title_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_title(request):
    if request.method == "POST":
        form = TitleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Title post addition was Successful')
            return redirect('view_title')
        else:
            messages.info(request, 'Title post addition was not Successful')
    else:
        form = TitleForm()
    context = {'key':'Add Type of Service', 'form': form}
    return render(request, 'backend/title_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_title(request, slug):
    title = get_object_or_404(Title, slug=slug)
    if request.method == "POST":
        form = TitleForm(request.POST or None, instance=title)
        if form.is_valid():
            form.save()
            messages.success(request, 'Title post update was Successful')
            return redirect('view_title')
        else:
            messages.info(request, 'Title post update was not Successful')
    else:
        form = TitleForm(instance=title)
    context = {'key':'Update Type of Service', 'form': form}
    return render(request, 'backend/title_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_title(request, slug):
    title = get_object_or_404(Title, slug=slug)
    if request.method == "POST":
        title.delete()
        messages.success(request, 'Title post was deleted Successfully')
        return redirect('view_title')
    context = {'key':'Delete Type of Service', 'item':title}
    return render(request, 'backend/title_delete.html', context)
#  END OF SERVICE TITLE


# START OF SERVICE
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_service(request):
    service = Service.objects.all()
    context = {'key':'Service Page', 'service':service}
    return render(request, 'backend/service_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service post addition was Successful')
            return redirect('view_service')
        else:
            messages.info(request, 'Service post addition was not Successful')
    else:
        form = ServiceForm()
    context = {'key':'Add Service', 'form': form}
    return render(request, 'backend/service_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == "POST":
        form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service post update was Successful')
            return redirect('view_service')
        else:
            messages.info(request, 'Service post update was not Successful')
    else:
        form = ServiceForm(instance=service)
    context = {'key':'Update Service', 'form': form}
    return render(request, 'backend/service_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == "POST":
        service.delete()
        messages.success(request, 'Service post was deleted Successfully')
        return redirect('view_service')
    context = {'key':'Delete Service', 'item':service}
    return render(request, 'backend/service_delete.html', context)
#  END OF SERVICE


# START OF PURPOSE STATEMENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_purpose(request):
    purpose = Purpose.objects.all()
    context = {'key':'Purpose Page', 'purpose':purpose}
    return render(request, 'backend/purpose_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_purpose(request):
    if request.method == "POST":
        form = PurposeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purpose post addition was Successful')
            return redirect('view_purpose')
        else:
            messages.info(request, 'Purpose post addition was not Successful')
    else:
        form = PurposeForm()
    context = {'key':'Add Purpose', 'form': form}
    return render(request, 'backend/purpose_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_purpose(request, slug):
    purpose = get_object_or_404(Purpose, slug=slug)
    if request.method == "POST":
        form = PurposeForm(request.POST or None, request.FILES or None, instance=purpose)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purpose post update was Successful')
            return redirect('view_purpose')
        else:
            messages.info(request, 'Purpose post update was not Successful')
    else:
        form = PurposeForm(instance=purpose)
    context = {'key':'Update Purpose', 'form': form}
    return render(request, 'backend/purpose_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_purpose(request, slug):
    purpose = get_object_or_404(Purpose, slug=slug)
    if request.method == "POST":
        purpose.delete()
        messages.success(request, 'Statement Purpose post was deleted Successfully')
        return redirect('view_purpose')
    context = {'key':'Delete Statement Purpose', 'item':purpose}
    return render(request, 'backend/purpose_delete.html', context)
#  END OF PURPOSE STATEMENT


# START OF STATEMENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_statement(request):
    statement = Statement.objects.all()
    context = {'key':'Statement', 'statement':statement}
    return render(request, 'backend/statement_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_statement(request):
    if request.method == "POST":
        form = StatementForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statement post addition was Successful')
            return redirect('view_statement')
        else:
            messages.info(request, 'Statement post addition was not Successful')
    else:
        form = StatementForm()
    context = {'key':'Add Statement', 'form': form}
    return render(request, 'backend/statement_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_statement(request, slug):
    statement = get_object_or_404(Statement, slug=slug)
    if request.method == "POST":
        form = StatementForm(request.POST or None, request.FILES or None, instance=statement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statement post update was Successful')
            return redirect('view_statement')
        else:
            messages.info(request, 'Statement post update was not Successful')
    else:
        form = StatementForm(instance=statement)
    context = {'key':'Update Statement', 'form': form}
    return render(request, 'backend/statement_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_statement(request, slug):
    statement = get_object_or_404(Statement, slug=slug)
    if request.method == "POST":
        statement.delete()
        messages.success(request, 'Statement post was deleted Successfully')
        return redirect('view_statement')
    context = {'key':'Delete Statement', 'item':statement}
    return render(request, 'backend/statement_delete.html', context)
#  END OF STATEMENT


# START OF CAREER
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_career(request):
    career = Career.objects.all()
    context = {'key':'Career Page', 'career':career}
    return render(request, 'backend/career_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_career(request):
    if request.method == "POST":
        form = CareerForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career post addition was Successful')
            return redirect('view_career')
        else:
            messages.info(request, 'Career post addition was not Successful')
    else:
        form = CareerForm()
    context = {'key':'Add Career', 'form': form}
    return render(request, 'backend/career_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_career(request, slug):
    career = get_object_or_404(Career, slug=slug)
    if request.method == "POST":
        form = CareerForm(request.POST or None, request.FILES or None, instance=career)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career post update was Successful')
            return redirect('view_career')
        else:
            messages.info(request, 'Career post update was not Successful')
    else:
        form = CareerForm(instance=career)
    context = {'key':'Update Career', 'form': form}
    return render(request, 'backend/career_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_career(request, slug):
    career = get_object_or_404(Career, slug=slug)
    if request.method == "POST":
        career.delete()
        messages.success(request, 'Career post was deleted Successfully')
        return redirect('view_career')
    context = {'key':'Delete Career', 'item':career}
    return render(request, 'backend/career_delete.html', context)
#  END OF CAREER


# START OF TEAM
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_team(request):
    team = Team.objects.filter(team=request.user)
    context = {'key':'Team', 'team':team}
    return render(request, 'backend/team_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_allteam(request):
    team = Team.objects.all()
    context = {'key':'Team', 'team':team}
    return render(request, 'backend/teamall_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.team = request.user
            instance.save()
            messages.success(request, 'Team post addition was Successful')
            return redirect('view_team')
        else:
            messages.info(request, 'Team post addition was not Successful')
    else:
        form = TeamForm()
    context = {'key':'Add Team', 'form': form}
    return render(request, 'backend/team_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_team(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if request.method == "POST":
        form = TeamForm(request.POST or None, request.FILES or None, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team post update was Successful')
            return redirect('view_team')
        else:
            messages.info(request, 'Team post update was not Successful')
    else:
        form = TeamForm(instance=team)
    context = {'key':'Update Team', 'form': form}
    return render(request, 'backend/team_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_team(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if request.method == "POST":
        team.delete()
        messages.success(request, 'Team post was deleted Successfully')
        return redirect('view_team')
    context = {'key':'Delete Team', 'item':team}
    return render(request, 'backend/team_delete.html', context)
#  END OF TEAM


# START OF TESTIMONY
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_testimony(request):
    testimony = Testimony.objects.all()
    context = {'key':'Testimony Page', 'testimony':testimony}
    return render(request, 'backend/testimony_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_testimony(request):
    if request.method == "POST":
        form = TestimonyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimony post addition was Successful')
            return redirect('view_testimony')
        else:
            messages.info(request, 'Testimony post addition was not Successful')
    else:
        form = TestimonyForm()
    context = {'key':'Add Testimony', 'form': form}
    return render(request, 'backend/testimony_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_testimony(request, slug):
    testimony = get_object_or_404(Testimony, slug=slug)
    if request.method == "POST":
        form = TestimonyForm(request.POST or None, request.FILES or None, instance=testimony)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimony post update was Successful')
            return redirect('view_testimony')
        else:
            messages.info(request, 'Testimony post update was not Successful')
    else:
        form = TestimonyForm(instance=testimony)
    context = {'key':'Update Testimony', 'form': form}
    return render(request, 'backend/testimony_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_testimony(request, slug):
    testimony = get_object_or_404(Testimony, slug=slug)
    if request.method == "POST":
        testimony.delete()
        messages.success(request, 'Testimony post was deleted Successfully')
        return redirect('view_testimony')
    context = {'key':'Delete Testimony', 'item':testimony}
    return render(request, 'backend/testimony_delete.html', context)
#  END OF TESTIMONY


# START OF ADVERT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_advert(request):
    advert = Advert.objects.all()
    context = {'key':'Advert', 'advert':advert}
    return render(request, 'backend/advert_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_advert(request):
    if request.method == "POST":
        form = AdvertForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advert post addition was Successful')
            return redirect('view_advert')
        else:
            messages.info(request, 'Advert post addition was not Successful')
    else:
        form = AdvertForm()
    context = {'key':'Add Advert', 'form': form}
    return render(request, 'backend/advert_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug)
    if request.method == "POST":
        form = AdvertForm(request.POST or None, request.FILES or None, instance=advert)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advert post update was Successful')
            return redirect('view_advert')
        else:
            messages.info(request, 'Advert post update was not Successful')
    else:
        form = AdvertForm(instance=advert)
    context = {'key':'Update Advert', 'form': form}
    return render(request, 'backend/advert_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug)
    if request.method == "POST":
        advert.delete()
        messages.success(request, 'Advert post was deleted Successfully')
        return redirect('view_advert')
    context = {'key':'Delete Advert', 'item':advert}
    return render(request, 'backend/advert_delete.html', context)
#  END OF ADVERT


# START OF OCCUPATION
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_occupation(request):
    occupation = Occupation.objects.all()
    context = {'key':'View Profession', 'occupation':occupation}
    return render(request, 'backend/occupation_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_occupation(request):
    if request.method == "POST":
        form = OccupationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Occupation post addition was Successful')
            return redirect('view_occupation')
        else:
            messages.info(request, 'Occupation post addition was not Successful')
    else:
        form = OccupationForm()
    context = {'key':'Add Profession', 'form': form}
    return render(request, 'backend/occupation_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_occupation(request, slug):
    occupation = get_object_or_404(Occupation, slug=slug)
    if request.method == "POST":
        form = OccupationForm(request.POST or None, instance=occupation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Occupation post update was Successful')
            return redirect('view_occupation')
        else:
            messages.info(request, 'Occupation post update was not Successful')
    else:
        form = OccupationForm(instance=occupation)
    context = {'key':'Update Profession', 'form': form}
    return render(request, 'backend/occupation_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_occupation(request, slug):
    occupation = get_object_or_404(Occupation, slug=slug)
    if request.method == "POST":
        occupation.delete()
        messages.success(request, 'Occupation post was deleted Successfully')
        return redirect('view_occupation')
    context = {'key':'Delete Profession', 'item':occupation}
    return render(request, 'backend/occupation_delete.html', context)
#  END OF OCCUPATION


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
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_loanpdf(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    pdf = render_to_pdf('invoice/loan.html', {'loan':loan, 'key':'Generated PDF for Loan'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Loan Application Form for %s.pdf" %loan.applicant.get_full_name
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE LOAN PDF 

# START OF GENERATE LOAN INVOICE PDF 
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_loanpaymentpdf(request, loanpayment_id):
    loan = get_object_or_404(Loan, pk=loanpayment_id)
    pdf = render_to_pdf('invoice/loan_payment.html', {'loan':loan, 'key':'Generated PDF for Loan Payment Advice'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Loan Payment Advice for %s.pdf" %loan.applicant.get_full_name
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE LOAN INVOICE PDF 


# TO VIEW PDF LOAN
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def render_loanpdf_view(request):
    loan = Loan.objects.filter(status=1)
    template_path = 'invoice/loan_invoice.html'
    context = {'loan': loan, 'key':'Loan Granted Analysis'}
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


# START OF GENERATE INVESTMENT PDF 
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_investmentpdf(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    pdf = render_to_pdf('invoice/investment.html', {'investment':investment, 'key':'Generated PDF for Investment'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Investment Acknowledgement for %s.pdf" %investment.investor.get_full_name
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE INVESTMENT PDF 

# START OF GENERATE INVESTMENT INVOICE PDF 
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def generate_investmentpaymentpdf(request, investmentpayment_id):
    investment = get_object_or_404(Investment, pk=investmentpayment_id)
    pdf = render_to_pdf('invoice/investment_payment.html', {'investment':investment, 'key':'Generated PDF for Investment Payment Advice'})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Investment Payment Advice for %s.pdf" %investment.investor.get_full_name
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
# END OF GENERATE INVESTMENT INVOICE PDF 


# TO VIEW PDF INVESTMENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def render_investmentpdf_view(request):
    investment = Investment.objects.filter(status=1)
    template_path = 'invoice/investment_invoice.html'
    context = {'investment': investment, 'key':'Investment Analysis'}
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



# START OF FAQ
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_faq(request):
    faq = Faq.objects.all()
    context = {'key':'FAQ Page', 'faq':faq}
    return render(request, 'backend/faq_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_faq(request):
    if request.method == "POST":
        form = FaqForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faq post addition was Successful')
            return redirect('view_faq')
        else:
            messages.info(request, 'Faq post addition was not Successful')
    else:
        form = FaqForm()
    context = {'key':'Add FAQ', 'form': form}
    return render(request, 'backend/faq_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_faq(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    if request.method == "POST":
        form = FaqForm(request.POST or None, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was Successful')
            return redirect('view_faq')
        else:
            messages.info(request, 'Post update was not Successful')
    else:
        form = FaqForm(instance=faq)
    context = {'key':'Update FAQ', 'form': form}
    return render(request, 'backend/faq_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_faq(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    if request.method == "POST":
        faq.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('view_faq')
    context = {'key':'Delete FAQ', 'item':faq}
    return render(request, 'backend/faq_delete.html', context)
#  END OF FAQ


# START OF EVENT
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_event(request):
    event = Event.objects.all()
    context = {'key':'Event', 'event':event}
    return render(request, 'backend/event_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post addition was Successful')
            return redirect('view_event')
        else:
            messages.info(request, 'Post addition was not Successful')
    else:
        form = EventForm()
    context = {'key':'Add Event', 'form': form}
    return render(request, 'backend/event_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        form = EventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was Successful')
            return redirect('view_event')
        else:
            messages.info(request, 'Post update was not Successful')
    else:
        form = EventForm(instance=event)
    context = {'key':'Update Event', 'form': form}
    return render(request, 'backend/event_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        event.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('view_event')
    context = {'key':'Delete Event', 'item':event}
    return render(request, 'backend/event_delete.html', context)
#  END OF EVENT


# START OF GALLERY
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_gallery(request):
    gallery = Gallery.objects.all()
    context = {'key':'Gallery', 'gallery':gallery}
    return render(request, 'backend/gallery_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post addition was Successful')
            return redirect('view_gallery')
        else:
            messages.info(request, 'Post addition was not Successful')
    else:
        form = GalleryForm()
    context = {'key':'Add Gallery', 'form': form}
    return render(request, 'backend/gallery_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_gallery(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    if request.method == "POST":
        form = GalleryForm(request.POST or None, request.FILES or None, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was Successful')
            return redirect('view_gallery')
        else:
            messages.info(request, 'Post update was not Successful')
    else:
        form = GalleryForm(instance=gallery)
    context = {'key':'Update Gallery', 'form': form}
    return render(request, 'backend/gallery_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_gallery(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    if request.method == "POST":
        gallery.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('view_gallery')
    context = {'key':'Gallery', 'item':gallery}
    return render(request, 'backend/gallery_delete.html', context)
#  END OF GALLERY


# START OF HEADER LOGO
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_header(request):
    header = HeaderLogo.objects.all()
    context = {'key':'Header Logo', 'header':header}
    return render(request, 'backend/header_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_header(request):
    if request.method == "POST":
        form = HeaderLogoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post addition was Successful')
            return redirect('view_header')
        else:
            messages.info(request, 'Post addition was not Successful')
    else:
        form = HeaderLogoForm()
    context = {'key':'Add Header Logo', 'form': form}
    return render(request, 'backend/header_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_header(request, slug):
    header = get_object_or_404(HeaderLogo, slug=slug)
    if request.method == "POST":
        form = HeaderLogoForm(request.POST or None, request.FILES or None, instance=header)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was Successful')
            return redirect('view_header')
        else:
            messages.info(request, 'Post update was not Successful')
    else:
        form = HeaderLogoForm(instance=header)
    context = {'key':'Update Header Logo', 'form': form}
    return render(request, 'backend/header_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_header(request, slug):
    header = get_object_or_404(HeaderLogo, slug=slug)
    if request.method == "POST":
        header.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('view_header')
    context = {'key':'Delete Header Logo', 'item':header}
    return render(request, 'backend/header_delete.html', context)
#  END OF HEADER LOGO


# START OF FOOTER LOGO
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_footer(request):
    footer = FooterLogo.objects.all()
    context = {'key':'Footer Logo', 'footer':footer}
    return render(request, 'backend/footer_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_footer(request):
    if request.method == "POST":
        form = FooterLogoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post addition was Successful')
            return redirect('view_footer')
        else:
            messages.info(request, 'Post addition was not Successful')
    else:
        form = FooterLogoForm()
    context = {'key':'Add Footer Logo', 'form': form}
    return render(request, 'backend/footer_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_footer(request, slug):
    footer = get_object_or_404(FooterLogo, slug=slug)
    if request.method == "POST":
        form = FooterLogoForm(request.POST or None, request.FILES or None, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post update was Successful')
            return redirect('view_footer')
        else:
            messages.info(request, 'Post update was not Successful')
    else:
        form = FooterLogoForm(instance=footer)
    context = {'key':'Update Footer Logo', 'form': form}
    return render(request, 'backend/footer_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_footer(request, slug):
    footer = get_object_or_404(FooterLogo, slug=slug)
    if request.method == "POST":
        footer.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('view_footer')
    context = {'key':'Delete Footer Logo', 'item':footer}
    return render(request, 'backend/footer_delete.html', context)
#  END OF FOOTER LOGO


# START OF LOAN DURATION
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_loanduration(request):
    duration = LoanDuration.objects.all()
    context = {'key':'Loan Duration', 'duration':duration}
    return render(request, 'application/loanduration_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_loanduration(request):
    if request.method == "POST":
        form = LoanDurationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Duration addition was Successful')
            return redirect('view_loanduration')
        else:
            messages.info(request, 'Loan Duration addition was not Successful')
    else:
        form = LoanDurationForm()
    context = {'key':'Loan Duration', 'form': form}
    return render(request, 'application/loanduration_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_loanduration(request, slug):
    duration = get_object_or_404(LoanDuration, slug=slug)
    if request.method == "POST":
        form = LoanDurationForm(request.POST or None, instance=duration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Duration update was Successful')
            return redirect('view_loanduration')
        else:
            messages.info(request, 'Loan Duration update was not Successful')
    else:
        form = LoanDurationForm(instance=duration)
    context = {'key':'Update Loan Duration', 'form': form}
    return render(request, 'application/loanduration_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_loanduration(request, slug):
    duration = get_object_or_404(LoanDuration, slug=slug)
    if request.method == "POST":
        duration.delete()
        messages.success(request, 'Loan Duration was deleted Successfully')
        return redirect('view_loanduration')
    context = {'key':'Delete Loan Duration', 'item':duration}
    return render(request, 'application/loanduration_delete.html', context)
#  END OF LOAN DURATION


# START OF LOAN INTEREST
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_loaninterest(request):
    interest = LoanInterest.objects.all()
    context = {'key':'Loan Interest', 'interest':interest}
    return render(request, 'application/loaninterest_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_loaninterest(request):
    if request.method == "POST":
        form = LoanInterestForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Interest addition was Successful')
            return redirect('view_loaninterest')
        else:
            messages.info(request, 'Loan Interest addition was not Successful')
    else:
        form = LoanInterestForm()
    context = {'key':'Loan Interest', 'form': form}
    return render(request, 'application/loaninterest_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def update_loaninterest(request, slug):
    interest = get_object_or_404(LoanInterest, slug=slug)
    if request.method == "POST":
        form = LoanInterestForm(request.POST or None, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Interest update was Successful')
            return redirect('view_loaninterest')
        else:
            messages.info(request, 'Loan Interest update was not Successful')
    else:
        form = LoanInterestForm(instance=interest)
    context = {'key':'Update Loan Interest', 'form': form}
    return render(request, 'application/loaninterest_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_loaninterest(request, slug):
    interest = get_object_or_404(LoanInterest, slug=slug)
    if request.method == "POST":
        interest.delete()
        messages.success(request, 'Loan Interest was deleted Successfully')
        return redirect('view_loaninterest')
    context = {'key':'Delete Loan Interest', 'item':interest}
    return render(request, 'application/loaninterest_delete.html', context)
#  END OF LOAN INTEREST


# START OF INVESTMENT INTEREST
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def view_investmentinterest(request):
    interest = InvestmentInterest.objects.all()
    context = {'key':'Investment Interest', 'interest':interest}
    return render(request, 'application/investmentinterest_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def add_investmentinterest(request):
    if request.method == "POST":
        form = InvestmentInterestForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Interest addition was Successful')
            return redirect('view_investmentinterest')
        else:
            messages.info(request, 'Investment Interest addition was not Successful')
    else:
        form = InvestmentInterestForm()
    context = {'key':'Investment Interest', 'form': form}
    return render(request, 'application/investmentinterest_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def update_investmentinterest(request, slug):
    interest = get_object_or_404(InvestmentInterest, slug=slug)
    if request.method == "POST":
        form = InvestmentInterestForm(request.POST or None, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Interest update was Successful')
            return redirect('view_investmentinterest')
        else:
            messages.info(request, 'Investment Interest update was not Successful')
    else:
        form = InvestmentInterestForm(instance=interest)
    context = {'key':'Update Investment Interest', 'form': form}
    return render(request, 'application/investmentinterest_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_investmentinterest(request, slug):
    interest = get_object_or_404(InvestmentInterest, slug=slug)
    if request.method == "POST":
        interest.delete()
        messages.success(request, 'Investment Interest was deleted Successfully')
        return redirect('view_investmentinterest')
    context = {'key':'Delete Investment Interest', 'item':interest}
    return render(request, 'application/investmentinterest_delete.html', context)
#  END OF INVESTMENT INTEREST


# START OF INVESTMENT DURATION
@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def view_investmentduration(request):
    duration = InvestmentDuration.objects.all()
    context = {'key':'Investment Duration', 'duration':duration}
    return render(request, 'application/investmentduration_view.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def add_investmentduration(request):
    if request.method == "POST":
        form = InvestmentDurationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Duration addition was Successful')
            return redirect('view_investmentduration')
        else:
            messages.info(request, 'Investment Duration addition was not Successful')
    else:
        form = InvestmentDurationForm()
    context = {'key':'Investment Duration', 'form': form}
    return render(request, 'application/investmentduration_add.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def update_investmentduration(request, slug):
    duration = get_object_or_404(InvestmentDuration, slug=slug)
    if request.method == "POST":
        form = InvestmentDurationForm(request.POST or None, instance=duration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment Duration update was Successful')
            return redirect('view_investmentduration')
        else:
            messages.info(request, 'Investment Duration update was not Successful')
    else:
        form = InvestmentDurationForm(instance=duration)
    context = {'key':'Update Investment Duration', 'form': form}
    return render(request, 'application/investmentduration_update.html', context)

@login_required(login_url='log_in')
@allowed_users(allowed_roles=["admin"])
def delete_investmentduration(request, slug):
    duration = get_object_or_404(InvestmentDuration, slug=slug)
    if request.method == "POST":
        duration.delete()
        messages.success(request, 'Investment Duration was deleted Successfully')
        return redirect('view_investmentduration')
    context = {'key':'Delete Investment Duration', 'item':duration}
    return render(request, 'application/investmentduration_delete.html', context)
#  END OF INVESTMENT DURATION

