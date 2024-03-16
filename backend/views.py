from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import Group
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on
from applications.models import Requirement
from newsletter.models import Mails
from account.models import User
from frontend.models import Tags, Category, About, News, Services, Blog, Privacy, Testimonial, Contact, Details, Advert, Statement, Career, Header, Footer, Faq, ServiceHeader, FAQHeader, TestimonialHeader, AboutHeader, CareerHeader, ContactHeader, Steps
from frontend.forms import TagsForm, CategoryForm, AboutForm, NewsForm, ServicesForm, BlogForm, PrivacyForm,  StatusBlogForm, TestimonialForm, ContactForm, DetailsForm, AdvertForm, StatementForm, CareerForm, HeaderForm, FooterForm, FaqForm, ServiceHeaderForm, FAQHeaderForm, TestimonialHeaderForm, AboutHeaderForm, ContactHeaderForm, CareerHeaderForm, StepsForm
from backend.models import Profile
from backend.forms import ProfileForm, ProfilePictureForm,  ChangePasswordForm, SuperUserForm, EditSuperUserForm, StaffUserForm, EditStaffUserForm, EditUserForm, ActionUserForm
from backend.decorators import allowed_users
# Create your views here.


# Start of Dashboard
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
@force_maintenance_mode_off
def dashboard(request):
    requirement = Requirement.objects.all()
    user = request.user
    mails = user.recipient.all()
    mails_count = mails.filter(is_read=False).count()
    context = {'title':'Dashboard', 'requirement':requirement, 'mails':mails, 'mails_count':mails_count}
    return render(request, 'backend/dashboard/index.html', context)
# End of Dashboard

# Start of Profile Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def profile(request, username):
    account    = get_object_or_404(User, username=username)

    context = {'title':'Personal Profile', 'account':account,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/profiles/profile.html', context)
# End of Profile Page

# Start of Staff Profile Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def staffprofiles(request):
    profiles = User.objects.filter(is_staff=True)
    context = {'title':'Profiles', 'profiles':profiles,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/profiles/staffprofiles.html', context)
# End of Staff Profile Page

# Start of Clients Profile Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def profiles(request):
    profiles = User.objects.filter(is_active=True).exclude(is_superuser=True).exclude(is_staff=True)
    context = {'title':'Profiles', 'profiles':profiles,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/profiles/profiles.html', context)
# End of Clients Profile Page

# Start of Profile Picture Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def change_picture(request):
    if request.method == "POST":
        pic_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if pic_form.is_valid():
            pic_form.save()
            messages.success(request, 'Your Passport was uploaded successfully')
            return redirect('edit-profile')
        else:
            messages.warning(request, 'Your Passport was not uploaded successfully')
        
    else:
        pic_form = ProfilePictureForm(instance=request.user.profile)
# End of Profile Picture Page

# Start of Edit Profile Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Information was updated successfully')
            return redirect('edit-profile')
        else:
            form.errors
            messages.warning(request, 'Your Profile Information was not updated, please rectify the errors')
    else:
        form = ProfileForm(instance=profile)
    context = {'title':'Edit Profile', 'profile':profile, 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/profiles/edit_profile.html', context)
# End of Edit Profile Page

# Start of Edit User Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = EditUserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was updated successfully')
            return redirect('edit-user')
        else:
            form.errors
            messages.warning(request, 'Your account was not updated, please rectify the errors')    
    else:
        form= EditUserForm(instance=user)
    context = {'title':'Update User', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/profiles/edit_user.html', context)
# End of Edit User Page


# Start of Change of Password Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your account password was changed successfully')
            return redirect('change-password')
        else:
            form.errors
            messages.warning(request, 'Your account password was not changed, please rectify the errors')
    else:
        form = ChangePasswordForm(request.user)
    context = {'title':'Update User', 'form': form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/change_password.html', context)
# End of Change of Password Page

# Start of Banned User
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_banned(request):
    users = User.objects.filter(is_active=False)
    context = {'title':'View Banned Users', 'users': users,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/banned_user.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_banneduser(request, slug):
    users = get_object_or_404(User, slug=slug)
    if request.method == "POST":
        form = ActionUserForm(request.POST or None, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account is now active and restored')
            return redirect('view-banned')
        else:
            form.errors
            messages.warning(request, 'User account was not active, please rectify the errors')
    else:
        form = ActionUserForm(instance=users)
        
    context = {'title':'Edit Banned User', 'form':form, 'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/edit_alluser.html', context)
# End of Banned User


# Start of Staff User
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_staffuser(request):
    users = User.objects.filter(is_staff=True, is_active=True).exclude(is_superuser=True)
    context = {'title':'View Staff Users', 'users':users,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/staff/view_staffuser.html', context)


@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def staff_user(request):
    if request.method == "POST":
        form = StaffUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group)
            email = request.POST['email']
            messages.success(request, f'Account creation for Staff User with this email "{email}" was successful')
            return redirect('view-staffuser')
        else:
            form.errors
            messages.warning(request, 'Account creation for Staff User was not successful, please rectify the errors')
    else:
        form = StaffUserForm()
    context = {'title':'Add Staff User', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/staff/staffuser.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_staffuser(request, slug):
    users = get_object_or_404(User, slug=slug)
    if request.method == "POST":
        form = EditStaffUserForm(request.POST or None, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff user account was deactivated successfully')
            return redirect('view-staffuser')
        else:
            form.errors
            messages.warning(request, 'Staff user account was not deactivated, please rectify the errors')
    else:
        form = EditStaffUserForm(instance=users)
    context = {'title':'Edit Staff User', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/staff/edit_staffuser.html', context)
# End of Staff User


# Start of Regular User
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_user(request):
    users = User.objects.filter(is_active=True).exclude(is_staff=True).exclude(is_superuser=True)
    context = {'title':'View Users', 'users': users,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/view_user.html', context)
# End of Regular User


# Start of Super User
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def super_user(request):
    if request.method == "POST":
        form = SuperUserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            email = request.POST['email']
            messages.success(request, f'Account creation for Super User with this email "{email}" was successful')
            return redirect('view-superuser')
        else:
            form.errors
            messages.warning(request, 'Account creation for Super User was not successful, please rectify the errors')
    else:
        form = SuperUserForm()
    context = {'title':'Add Super User', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/super/superuser.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_superuser(request):
    users = User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
    context = {'title':'View Super Users', 'users':users,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/super/view_superuser.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_superuser(request, slug):
    users = get_object_or_404(User, slug=slug)
    if request.method == "POST":
        form = EditSuperUserForm(request.POST or None, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'Super user account was deactivated successfully')
            return redirect('view-superuser')
        else:
            form.errors
            messages.warning(request, 'Super user account was not deactivated, please rectify the errors')
    else:
        form = EditSuperUserForm(instance=users)
    context = {'title':'Edit Super User', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/super/edit_superuser.html', context)
# End of Super User

# Start of All Users
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def all_user(request):
    users = User.objects.all().exclude(is_active=False).exclude(is_superuser=True)
    context = {'title':'View All Users', 'users': users, 'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/all_user.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def edit_alluser(request, slug):
    users = get_object_or_404(User, slug=slug)
    if request.method == "POST":
        form = ActionUserForm(request.POST or None, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account was deactivated successfully')
            return redirect('all-user')
        else:
            form.errors
            messages.warning(request, 'User account was not deactivated, please rectify the errors')
    else:
        form = ActionUserForm(instance=users)
        
    context = {'title':'Edit User', 'form':form, 'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/edit_alluser.html', context)


@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin"])
def delete_alluser(request, slug):
    users = get_object_or_404(User, slug=slug)
    if request.method == "POST":
        users.delete()
        messages.success(request, 'User account was deleted successfully')
        return redirect('all-user')
    context = {'title':'Delete User', 'users':users,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/users/regular/delete_alluser.html', context)
# End of All Users

# Start of About Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_about(request):
    if request.method == "POST":
        form = AboutForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'About Post was created successfully')
            return redirect('view-about')
        else:
            form.errors
            messages.warning(request, 'About Post was not created, please rectify the errors')
    else:
        form = AboutForm()
    context = {'title':'About Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/about/add_about.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_about(request):
    about = About.objects.all()
    context = {'title':'View About Post', 'about':about,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/about/view_about.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_about(request, slug):
    about = get_object_or_404(About, slug=slug)
    if request.method == "POST":
        form = AboutForm(request.POST or None, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'About Post was updated successfully')
            return redirect('view-about')
        else:
            form.errors
            messages.warning(request, 'About Post was not updated, please rectify the errors')
    else:
        form = AboutForm(instance=about)
    context = {'title':'Update About Post', 'about':about, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/about/edit_about.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_about(request, slug):
    about = get_object_or_404(About, slug=slug)
    if request.method == "POST":
        about.delete()
        messages.success(request, 'About Post was deleted successfully')
        return redirect('view-about')
    context = {'title':'Delete About Post', 'about':about,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/about/delete_about.html', context)
# End of About Page


#  Start of Advert Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_advert(request):
    if request.method == "POST":
        form = AdvertForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advert Post was created successfully')
            return redirect('view-advert')
        else:
            form.errors
            messages.warning(request, 'Advert Post was not created, please rectify the errors')
    else:
        form = AdvertForm()
    context = {'title':'Advert Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/advert/add_advert.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_advert(request):
    advert = Advert.objects.all()
    context = {'title':'View Advert Post', 'advert':advert,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/advert/view_advert.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug)
    if request.method == "POST":
        form = AdvertForm(request.POST or None, request.FILES, instance=advert)
        if form.is_valid():
            form.save()
            messages.success(request, 'Advert Post was updated successfully')
            return redirect('view-advert')
        else:
            form.errors
            messages.warning(request, 'Advert Post was not updated, please rectify the errors')
    else:
        form = AdvertForm(instance=advert)
    context = {'title':'Update Advert Post', 'advert':advert, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/advert/edit_advert.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_advert(request, slug):
    advert = get_object_or_404(Advert, slug=slug)
    if request.method == "POST":
        advert.delete()
        messages.success(request, 'Advert Post was deleted successfully')
        return redirect('view-advert')
    context = {'title':'Delete Advert Post', 'advert':advert,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/advert/delete_advert.html', context)
# End of Advert Page


#  Start of Blog Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'Post was created successfully')
            return redirect('view-blog')
        else:
            form.errors
            messages.warning(request, 'Post was not created, please rectify the errors')
    else:
        form = BlogForm()
    context = {'title':'Blog Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/add_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_blog(request):
    blog = Blog.objects.all()
    context = {'title':'View Blog Post', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/view_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        form = BlogForm(request.POST or None, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post was updated successfully')
            return redirect('view-blog')
        else:
            form.errors
            messages.warning(request, 'Post was not updated, please rectify the errors')
    else:
        form = BlogForm(instance=blog)
    context = {'title':'Update Blog Post', 'blog':blog, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/edit_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        blog.delete()
        messages.success(request, 'Post was deleted successfully')
        return redirect('view-blog')
    context = {'title':'Delete Blog Post', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/delete_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def approve_blog_view(request):
    blog = Blog.objects.all()
    context = {'title':'Approve Blog View', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/approve_blog_view.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def approve_blog(request, slug):
    approve = get_object_or_404(Blog, slug=slug)
    approve.status = 1
    approve.save()
    messages.success(request, 'Post approval was successful')
    return redirect('approve-blogview')
    

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def disapprove_blog(request, slug):
    disapprove = get_object_or_404(Blog, slug=slug)
    disapprove.status = 2
    disapprove.save()
    messages.warning(request, 'Post approval was not successful')
    return redirect('approve-blogview')

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def blog_pending(request):
    blog = Blog.objects.filter(status=0)
    context = {'title':'Pending Blog', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/pending_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def blog_approve(request):
    blog = Blog.objects.filter(status=1)
    context = {'title':'Approve Blog', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/approve_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def blog_disapprove(request):
    blog = Blog.objects.filter(status=2)
    context = {'title':'Disapprove Blog', 'blog':blog,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/disapprove_blog.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def status_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        form = StatusBlogForm(request.POST or None, request.FILES or None, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Status was edited successfully')
            return redirect('approve-blogview')
        else:
            form.errors
            messages.warning(request, 'Post Status was not edited successfully')
    else:
        form = StatusBlogForm(instance=blog)
    context = {'title':'Edit Blog Status Form', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/blog/status_blog.html', context)
# End of Blog Page



#  Start of Career Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_career(request):
    if request.method == "POST":
        form = CareerForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career Post was created successfully')
            return redirect('view-career')
        else:
            form.errors
            messages.warning(request, 'Career Post was not created, please rectify the errors')
    else:
        form = CareerForm()
    context = {'title':'Career Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/career/add_career.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_career(request):
    career = Career.objects.all()
    context = {'title':'View Career Post', 'career':career,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/career/view_career.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_career(request, slug):
    career = get_object_or_404(Career, slug=slug)
    if request.method == "POST":
        form = CareerForm(request.POST or None, request.FILES, instance=career)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career Post was updated successfully')
            return redirect('view-career')
        else:
            form.errors
            messages.warning(request, 'Career Post was not updated, please rectify the errors')
    else:
        form = CareerForm(instance=career)
    context = {'title':'Update Career Post', 'career':career, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/career/edit_career.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_career(request, slug):
    career = get_object_or_404(Career, slug=slug)
    if request.method == "POST":
        career.delete()
        messages.success(request, 'Career Post was deleted successfully')
        return redirect('view-career')
    context = {'title':'Delete Career Post', 'career':career,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/career/delete_career.html', context)
# End of Career Page


# Start of Category Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Post was created successfully')
            return redirect('view-category')
        else:
            form.errors
            messages.warning(request, 'Category Post was not created, please rectify the errors')
    else:
        form = CategoryForm()
    context = {'title':'Category Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/category/add_category.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_category(request):
    category = Category.objects.all()
    context = {'title':'View Category Post', 'category':category,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/category/view_category.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = CategoryForm(request.POST or None, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Post was updated successfully')
            return redirect('view-category')
        else:
            form.errors
            messages.warning(request, 'Category Post was not updated, please rectify the errors')
    else:
        form = CategoryForm(instance=category)
    context = {'title':'Update Category Post', 'category':category, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/category/edit_category.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        category.delete()
        messages.success(request, 'Category Post was deleted successfully')
        return redirect('view-category')
    context = {'title':'Delete Category Post', 'category':category,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/category/delete_category.html', context)
# End of Category Page


# Start of Contact Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_contact(request):
    contact = Contact.objects.all()
    context = {'title':'View Contact Post', 'contact':contact,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contact/view_contact.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_contact(request, slug):
    contact = get_object_or_404(Contact, slug=slug)
    if request.method == "POST":
        form = ContactForm(request.POST or None, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Post was updated successfully')
            return redirect('view-contact')
        else:
            form.errors
            messages.warning(request, 'Contact Post was not updated, please rectify the errors')
    else:
        form = ContactForm(instance=contact)
    context = {'title':'Update Contact Post', 'contact':contact, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contact/edit_contact.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_contact(request, slug):
    contact = get_object_or_404(Contact, slug=slug)
    if request.method == "POST":
        contact.delete()
        messages.success(request, 'Contact Post was deleted successfully')
        return redirect('view-contact')
    context = {'title':'Delete Contact Post', 'contact':contact,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contact/delete_contact.html', context)
# End of Contact Page


# Start of Contact Details Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_detail(request):
    if request.method == "POST":
        form = DetailsForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Detail Post was created successfully')
            return redirect('view-detail')
        else:
            form.errors
            messages.warning(request, 'Contact Detail Post was not created, please rectify the errors')
    else:
        form = DetailsForm()
    context = {'title':'Contact Detail Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/detail/add_detail.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_detail(request):
    detail = Details.objects.all()
    context = {'title':'View Contact Detail Post', 'detail':detail,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/detail/view_detail.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_detail(request, slug):
    detail = get_object_or_404(Details, slug=slug)
    if request.method == "POST":
        form = DetailsForm(request.POST or None, request.FILES, instance=detail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Detail Post was updated successfully')
            return redirect('view-detail')
        else:
            form.errors
            messages.warning(request, 'Contact Detail Post was not updated, please rectify the errors')
    else:
        form = DetailsForm(instance=detail)
    context = {'title':'Update Contact Detail Post', 'detail':detail, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/detail/edit_detail.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_detail(request, slug):
    detail= get_object_or_404(Details, slug=slug)
    if request.method == "POST":
        detail.delete()
        messages.success(request, 'Contact Detail Post was deleted successfully')
        return redirect('view-detail')
    context = {'title':'Delete Contact Detail Post', 'detail':detail,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/detail/delete_detail.html', context)
# End of Contact Details Page


# Start of Services Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_service(request):
    if request.method == "POST":
        form = ServicesForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Post was created successfully')
            return redirect('view-service')
        else:
            form.errors
            messages.warning(request, 'Service Post was not created, please rectify the errors')
    else:
        form = ServicesForm()
    context = {'title':'Service Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/services/add_service.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_service(request):
    service = Services.objects.all()
    context = {'title':'View Service Post', 'service':service,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/services/view_service.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_service(request, slug):
    service = get_object_or_404(Services, slug=slug)
    if request.method == "POST":
        form = ServicesForm(request.POST or None, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Post was updated successfully')
            return redirect('view-service')
        else:
            form.errors
            messages.warning(request, 'Service Post was not updated, please rectify the errors')
    else:
        form = ServicesForm(instance=service)
    context = {'title':'Update Service Post', 'service':service, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/services/edit_service.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_service(request, slug):
    service = get_object_or_404(Services, slug=slug)
    if request.method == "POST":
        service.delete()
        messages.success(request, 'Service Post was deleted successfully')
        return redirect('view-service')
    context = {'title':'Delete Service Post', 'service':service,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/services/delete_service.html', context)
# End of Services Page


# Start of Statement Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_statement(request):
    if request.method == "POST":
        form = StatementForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statement Post was created successfully')
            return redirect('view-statement')
        else:
            form.errors
            messages.warning(request, 'Statement Post was not created, please rectify the errors')
    else:
        form = StatementForm()
    context = {'title':'Statement Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/statement/add_statement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_statement(request):
    statement = Statement.objects.all()
    context = {'title':'View Statement Post', 'statement':statement,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/statement/view_statement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_statement(request, slug):
    statement = get_object_or_404(Statement, slug=slug)
    if request.method == "POST":
        form = StatementForm(request.POST or None, request.FILES, instance=statement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statement Post was updated successfully')
            return redirect('view-statement')
        else:
            form.errors
            messages.warning(request, 'Statement Post was not updated, please rectify the errors')
    else:
        form = StatementForm(instance=statement)
    context = {'title':'Update Statement Post', 'statement':statement, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/statement/edit_statement.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_statement(request, slug):
    statement = get_object_or_404(Statement, slug=slug)
    if request.method == "POST":
        statement.delete()
        messages.success(request, 'Statement Post was deleted successfully')
        return redirect('view-statement')
    context = {'title':'Delete Statement Post', 'statement':statement,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/statement/delete_statement.html', context)
# End of Statement Page


# Start of Tags Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_tag(request):
    if request.method == "POST":
        form = TagsForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag Post was created successfully')
            return redirect('view-tag')
        else:
            form.errors
            messages.warning(request, 'Tag Post was not created, please rectify the errors')
    else:
        form = TagsForm()
    context = {'title':'Tags Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/tag/add_tag.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_tag(request):
    tag = Tags.objects.all()
    context = {'title':'View Tag Post', 'tag':tag,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/tag/view_tag.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_tag(request, slug):
    tag = get_object_or_404(Tags, slug=slug)
    if request.method == "POST":
        form = TagsForm(request.POST or None, request.FILES, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag Post was updated successfully')
            return redirect('view-tag')
        else:
            form.errors
            messages.warning(request, 'Tag Post was not updated, please rectify the errors')
    else:
        form = TagsForm(instance=tag)
    context = {'title':'Update Tag Post', 'statement':tag, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/tag/edit_tag.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_tag(request, slug):
    tag = get_object_or_404(Tags, slug=slug)
    if request.method == "POST":
        tag.delete()
        messages.success(request, 'Tag Post was deleted successfully')
        return redirect('view-tag')
    context = {'title':'Delete Tag Post', 'tag':tag,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/tag/delete_tag.html', context)
# End of Tags Page


# Start of Testimonial Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_testimonial(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial Post was created successfully')
            return redirect('view-testimonial')
        else:
            form.errors
            messages.warning(request, 'Testimonial Post was not created, please rectify the errors')
    else:
        form = TestimonialForm()
    context = {'title':'Testimonial Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonial/add_testimonial.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_testimonial(request):
    testimonial = Testimonial.objects.all()
    context = {'title':'View Testimonial Post', 'testimonial':testimonial,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonial/view_testimonial.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_testimonial(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    if request.method == "POST":
        form = TestimonialForm(request.POST or None, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial Post was updated successfully')
            return redirect('view-testimonial')
        else:
            form.errors
            messages.warning(request, 'Testimonial Post was not updated, please rectify the errors')
    else:
        form = TestimonialForm(instance=testimonial)
    context = {'title':'Update Testimonial Post', 'testimonial':testimonial, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonial/edit_testimonial.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_testimonial(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, 'Testimonial Post was deleted successfully')
        return redirect('view-testimonial')
    context = {'title':'Delete Testimonial Post', 'testimonial':testimonial,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonial/delete_testimonial.html', context)
# End of Testimonial Page


# Start of News Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News Post was created successfully')
            return redirect('view-news')
        else:
            form.errors
            messages.warning(request, 'News Post was not created, please rectify the errors')
    else:
        form = NewsForm()
    context = {'title':'News Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/news/add_news.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_news(request):
    news = News.objects.all()
    context = {'title':'View News Post', 'news':news,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/news/view_news.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    if request.method == "POST":
        form = NewsForm(request.POST or None, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News Post was updated successfully')
            return redirect('view-news')
        else:
            form.errors
            messages.warning(request, 'News Post was not updated, please rectify the errors')
    else:
        form = NewsForm(instance=news)
    context = {'title':'Update News Post', 'news':news, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/news/edit_news.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    if request.method == "POST":
        news.delete()
        messages.success(request, 'News Post was deleted successfully')
        return redirect('view-news')
    context = {'title':'Delete News Post', 'news':news,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/news/delete_news.html', context)
# End of News Page


# Start of Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_header(request):
    if request.method == "POST":
        form = HeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Header Post was created successfully')
            return redirect('view-header')
        else:
            form.errors
            messages.warning(request, 'Header Post was not created, please rectify the errors')
    else:
        form = HeaderForm()
    context = {'title':'Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/header/add_header.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_header(request):
    header = Header.objects.all()
    context = {'title':'View Header Post', 'header':header,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/header/view_header.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_header(request, slug):
    header = get_object_or_404(Header, slug=slug)
    if request.method == "POST":
        form = HeaderForm(request.POST or None, request.FILES or None, instance=header)
        if form.is_valid():
            form.save()
            messages.success(request, 'Header Post was updated successfully')
            return redirect('view-header')
        else:
            form.errors
            messages.warning(request, 'Header Post was not updated, please rectify the errors')
    else:
        form = HeaderForm(instance=header)
    context = {'title':'Update Header Post', 'header':header, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/header/edit_header.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_header(request, slug):
    header = get_object_or_404(Header, slug=slug)
    if request.method == "POST":
        header.delete()
        messages.success(request, 'Header Post was deleted successfully')
        return redirect('view-header')
    context = {'title':'Delete Header Post', 'header':header,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/header/delete_header.html', context)
# End of Header Page


# Start of Footer Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_footer(request):
    if request.method == "POST":
        form = FooterForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer Post was created successfully')
            return redirect('view-footer')
        else:
            form.errors
            messages.warning(request, 'Footer Post was not created, please rectify the errors')
    else:
        form = FooterForm()
    context = {'title':'Footer Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/footer/add_footer.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_footer(request):
    footer = Footer.objects.all()
    context = {'title':'View Footer Post', 'footer':footer,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/footer/view_footer.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_footer(request, slug):
    footer = get_object_or_404(Footer, slug=slug)
    if request.method == "POST":
        form = FooterForm(request.POST or None, request.FILES or None, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer Post was updated successfully')
            return redirect('view-footer')
        else:
            form.errors
            messages.warning(request, 'Footer Post was not updated, please rectify the errors')
    else:
        form = FooterForm(instance=footer)
    context = {'title':'Update Footer Post', 'footer':footer, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/footer/edit_footer.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_footer(request, slug):
    footer = get_object_or_404(Footer, slug=slug)
    if request.method == "POST":
        footer.delete()
        messages.success(request, 'Footer Post was deleted successfully')
        return redirect('view-footer')
    context = {'title':'Delete Footer Post', 'footer':footer,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/footer/delete_footer.html', context)
# End of Footer Page


# Start of Faq Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_faq(request):
    if request.method == "POST":
        form = FaqForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faq Post was created successfully')
            return redirect('view-faq')
        else:
            form.errors
            messages.warning(request, 'Faq Post was not created, please rectify the errors')
    else:
        form = FaqForm()
    context = {'title':'Faq Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faq/add_faq.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_faq(request):
    faq = Faq.objects.all()
    context = {'title':'View Faq Post', 'faq':faq,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faq/view_faq.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_faq(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    if request.method == "POST":
        form = FaqForm(request.POST or None, request.FILES or None, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faq Post was updated successfully')
            return redirect('view-faq')
        else:
            form.errors
            messages.warning(request, 'Faq Post was not updated, please rectify the errors')
    else:
        form = FaqForm(instance=faq)
    context = {'title':'Update Faq Post', 'faq':faq, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faq/edit_faq.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_faq(request, slug):
    faq = get_object_or_404(Faq, slug=slug)
    if request.method == "POST":
        faq.delete()
        messages.success(request, 'Faq Post was deleted successfully')
        return redirect('view-faq')
    context = {'title':'Delete Faq Post', 'faq':faq,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faq/delete_faq.html', context)
# End of Faq Page

# Start of Steps Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_steps(request):
    if request.method == "POST":
        form = StepsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Steps Post was created successfully')
            return redirect('view-steps')
        else:
            form.errors
            messages.warning(request, 'Loan Steps Post was not created, please rectify the errors')
    else:
        form = StepsForm()
    context = {'title':'Loan Steps Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/steps/add_steps.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_steps(request):
    steps = Steps.objects.all()
    context = {'title':'View Steps Post', 'steps':steps,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/steps/view_steps.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_steps(request, slug):
    steps = get_object_or_404(Steps, slug=slug)
    if request.method == "POST":
        form = StepsForm(request.POST or None, request.FILES or None, instance=steps)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan Steps Post was updated successfully')
            return redirect('view-steps')
        else:
            form.errors
            messages.warning(request, 'Loan Steps Post was not updated, please rectify the errors')
    else:
        form = StepsForm(instance=steps)
    context = {'title':'Update Loan Steps Post', 'steps':steps, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/steps/edit_steps.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_steps(request, slug):
    steps = get_object_or_404(Steps, slug=slug)
    if request.method == "POST":
        steps.delete()
        messages.success(request, 'Loan Steps Post was deleted successfully')
        return redirect('view-steps')
    context = {'title':'Delete Loan Steps Post', 'steps':steps,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/steps/delete_steps.html', context)
# End of Step Page

# Start of Service Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_serviceheader(request):
    if request.method == "POST":
        form = ServiceHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Header Post was created successfully')
            return redirect('view-serviceheader')
        else:
            form.errors
            messages.warning(request, 'Service Header Post was not created, please rectify the errors')
    else:
        form = ServiceHeaderForm()
    context = {'title':'Service Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/serviceheader/add_serviceheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_serviceheader(request):
    serviceheader = ServiceHeader.objects.all()
    context = {'title':'View Service Header Post', 'serviceheader':serviceheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/serviceheader/view_serviceheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_serviceheader(request, slug):
    serviceheader = get_object_or_404(ServiceHeader, slug=slug)
    if request.method == "POST":
        form = ServiceHeaderForm(request.POST or None, request.FILES or None, instance=serviceheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service Header Post was updated successfully')
            return redirect('view-serviceheader')
        else:
            form.errors
            messages.warning(request, 'Service Header Post was not updated, please rectify the errors')
    else:
        form = ServiceHeaderForm(instance=serviceheader)
    context = {'title':'Update Service Header Post', 'serviceheader':serviceheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/serviceheader/edit_serviceheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_serviceheader(request, slug):
    serviceheader = get_object_or_404(ServiceHeader, slug=slug)
    if request.method == "POST":
        serviceheader.delete()
        messages.success(request, 'Service Header Post was deleted successfully')
        return redirect('view-serviceheader')
    context = {'title':'Delete Service Header Post', 'serviceheader':serviceheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/serviceheader/delete_serviceheader.html', context)
# End of Service Header Page


# Start of FAQ Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_faqheader(request):
    if request.method == "POST":
        form = FAQHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ Header Post was created successfully')
            return redirect('view-faqheader')
        else:
            form.errors
            messages.warning(request, 'FAQ Header Post was not created, please rectify the errors')
    else:
        form = FAQHeaderForm()
    context = {'title':'FAQ Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faqheader/add_faqheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_faqheader(request):
    faqheader = FAQHeader.objects.all()
    context = {'title':'View FAQ Header Post', 'faqheader':faqheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faqheader/view_faqheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_faqheader(request, slug):
    faqheader = get_object_or_404(FAQHeader, slug=slug)
    if request.method == "POST":
        form = FAQHeaderForm(request.POST or None, request.FILES or None, instance=faqheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ Header Post was updated successfully')
            return redirect('view-faqheader')
        else:
            form.errors
            messages.warning(request, 'FAQ Header Post was not updated, please rectify the errors')
    else:
        form = FAQHeaderForm(instance=faqheader)
    context = {'title':'Update FAQ Header Post', 'faqheader':faqheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faqheader/edit_faqheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_faqheader(request, slug):
    faqheader = get_object_or_404(FAQHeader, slug=slug)
    if request.method == "POST":
        faqheader.delete()
        messages.success(request, 'FAQ Header Post was deleted successfully')
        return redirect('view-faqheader')
    context = {'title':'Delete FAQ Header Post', 'faqheader':faqheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/faqheader/delete_faqheader.html', context)
# End of FAQ Header Page


# Start of TESTIMONIAL Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_testimonialheader(request):
    if request.method == "POST":
        form = TestimonialHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial Header Post was created successfully')
            return redirect('view-testimonialheader')
        else:
            form.errors
            messages.warning(request, 'Testimonial Header Post was not created, please rectify the errors')
    else:
        form = TestimonialHeaderForm()
    context = {'title':'Testimonial Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonialheader/add_testimonialheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_testimonialheader(request):
    testimonialheader = TestimonialHeader.objects.all()
    context = {'title':'View Testimonial Header Post', 'testimonialheader':testimonialheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonialheader/view_testimonialheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_testimonialheader(request, slug):
    testimonialheader = get_object_or_404(TestimonialHeader, slug=slug)
    if request.method == "POST":
        form = TestimonialHeaderForm(request.POST or None, request.FILES or None, instance=testimonialheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial Header Post was updated successfully')
            return redirect('view-testimonialheader')
        else:
            form.errors
            messages.warning(request, 'Testimonial Header Post was not updated, please rectify the errors')
    else:
        form = TestimonialHeaderForm(instance=testimonialheader)
    context = {'title':'Update Testimonial Header Post', 'testimonialheader':testimonialheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonialheader/edit_testimonialheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_testimonialheader(request, slug):
    testimonialheader = get_object_or_404(TestimonialHeader, slug=slug)
    if request.method == "POST":
        testimonialheader.delete()
        messages.success(request, 'Testimonial Header Post was deleted successfully')
        return redirect('view-testimonialheader')
    context = {'title':'Delete Testimonial Header Post', 'testimonialheader':testimonialheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/testimonialheader/delete_testimonialheader.html', context)
# End of TESTIMONIAL Header Page


# Start of ABOUT Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_aboutheader(request):
    if request.method == "POST":
        form = AboutHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'About Header Post was created successfully')
            return redirect('view-aboutheader')
        else:
            form.errors
            messages.warning(request, 'About Header Post was not created, please rectify the errors')
    else:
        form = AboutHeaderForm()
    context = {'title':'About Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/aboutheader/add_aboutheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_aboutheader(request):
    aboutheader = AboutHeader.objects.all()
    context = {'title':'View About Header Post', 'aboutheader':aboutheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/aboutheader/view_aboutheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_aboutheader(request, slug):
    aboutheader = get_object_or_404(AboutHeader, slug=slug)
    if request.method == "POST":
        form = AboutHeaderForm(request.POST or None, request.FILES or None, instance=aboutheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'About Header Post was updated successfully')
            return redirect('view-aboutheader')
        else:
            form.errors
            messages.warning(request, 'About Header Post was not updated, please rectify the errors')
    else:
        form = AboutHeaderForm(instance=aboutheader)
    context = {'title':'Update About Header Post', 'aboutheader':aboutheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/aboutheader/edit_aboutheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_aboutheader(request, slug):
    aboutheader = get_object_or_404(AboutHeader, slug=slug)
    if request.method == "POST":
        aboutheader.delete()
        messages.success(request, 'About Header Post was deleted successfully')
        return redirect('view-aboutheader')
    context = {'title':'Delete About Header Post', 'aboutheader':aboutheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/aboutheader/delete_aboutheader.html', context)
# End of ABOUT Header Page


# Start of Contact Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_contactheader(request):
    if request.method == "POST":
        form = ContactHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Header Post was created successfully')
            return redirect('view-contactheader')
        else:
            form.errors
            messages.warning(request, 'Contact Header Post was not created, please rectify the errors')
    else:
        form = ContactHeaderForm()
    context = {'title':'Contact Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contactheader/add_contactheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_contactheader(request):
    contactheader = ContactHeader.objects.all()
    context = {'title':'View Contact Header Post', 'contactheader':contactheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contactheader/view_contactheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_contactheader(request, slug):
    contactheader = get_object_or_404(ContactHeader, slug=slug)
    if request.method == "POST":
        form = ContactHeaderForm(request.POST or None, request.FILES or None, instance=contactheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Header Post was updated successfully')
            return redirect('view-contactheader')
        else:
            form.errors
            messages.warning(request, 'Contact Header Post was not updated, please rectify the errors')
    else:
        form = ContactHeaderForm(instance=contactheader)
    context = {'title':'Update Contact Header Post', 'contactheader':contactheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contactheader/edit_contactheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_contactheader(request, slug):
    contactheader = get_object_or_404(ContactHeader, slug=slug)
    if request.method == "POST":
        contactheader.delete()
        messages.success(request, 'Contact Header Post was deleted successfully')
        return redirect('view-contactheader')
    context = {'title':'Delete Contact Header Post', 'contactheader':contactheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/contactheader/delete_contactheader.html', context)
# End of Contact Header Page


# Start of Career Header Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_careerheader(request):
    if request.method == "POST":
        form = CareerHeaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career Header Post was created successfully')
            return redirect('view-careerheader')
        else:
            form.errors
            messages.warning(request, 'Career Header Post was not created, please rectify the errors')
    else:
        form = CareerHeaderForm()
    context = {'title':'Career Header Post', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/careerheader/add_careerheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_careerheader(request):
    careerheader = CareerHeader.objects.all()
    context = {'title':'View Career Header Post', 'careerheader':careerheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/careerheader/view_careerheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_careerheader(request, slug):
    careerheader = get_object_or_404(CareerHeader, slug=slug)
    if request.method == "POST":
        form = CareerHeaderForm(request.POST or None, request.FILES or None, instance=careerheader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career Header Post was updated successfully')
            return redirect('view-careerheader')
        else:
            form.errors
            messages.warning(request, 'Career Header Post was not updated, please rectify the errors')
    else:
        form = CareerHeaderForm(instance=careerheader)
    context = {'title':'Update Career Header Post', 'careerheader':careerheader, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/careerheader/edit_careerheader.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_careerheader(request, slug):
    careerheader = get_object_or_404(CareerHeader, slug=slug)
    if request.method == "POST":
        careerheader.delete()
        messages.success(request, 'Career Header Post was deleted successfully')
        return redirect('view-careerheader')
    context = {'title':'Delete Career Header Post', 'careerheader':careerheader,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/careerheader/delete_careerheader.html', context)
# End of Career Header Page



# Start of Privacy Page
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def add_privacy(request):
    if request.method == "POST":
        form = PrivacyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Privacy Post was created successfully')
            return redirect('view-privacy')
        else:
            form.errors
            messages.warning(request, 'Privacy Post was not created, please rectify the errors')
    else:
        form = PrivacyForm()
    context = {'title':'Privacy Post', 'form':form, 'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()
               }
    return render(request, 'backend/pages/privacy/add_privacy.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_privacy(request):
    privacy = Privacy.objects.all()
    context = {'title':'View Privacy Post', 'privacy':privacy, 'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()
               }
    return render(request, 'backend/pages/privacy/view_privacy.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_privacy(request, slug):
    privacy = get_object_or_404(Privacy, slug=slug)
    if request.method == "POST":
        form = PrivacyForm(request.POST or None, request.FILES or None, instance=privacy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Privacy Post was updated successfully')
            return redirect('view-privacy')
        else:
            form.errors
            messages.warning(request, 'Privacy Post was not updated, please rectify the errors')
    else:
        form = PrivacyForm(instance=privacy)
    context = {'title':'Update Privacy Post', 'privacy':privacy, 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()
               }
    return render(request, 'backend/pages/privacy/edit_privacy.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_privacy(request, slug):
    privacy = get_object_or_404(Privacy, slug=slug)
    if request.method == "POST":
        privacy.delete()
        messages.success(request, 'Privacy Post was deleted successfully')
        return redirect('view-privacy')
    context = {'title':'Delete Privacy Post', 'privacy':privacy,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'backend/pages/privacy/delete_privacy.html', context)
# End of Privacy Page


