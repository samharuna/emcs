from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from frontend.models import Post, Tags, Category, Comment, Reply, About, Service, Newsletter, Statement, Team, Testimony, Career, Advert, Contact, ContactDetail, Gallery, Faq, HeaderLogo, FooterLogo
from frontend.forms import CommentForm, ReplyForm, ContactForm, PostForm
from backend.forms import ProfileForm, UserForm
from backend.models import Profile
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from accounts.forms import SignUpForm, SignInForm, ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def home(request):
    service = Service.objects.all()[0:3]
    home = Post.objects.filter(status=1).order_by("-id")[0:4]
    latest_post = Post.objects.filter(status=1).order_by("-id")[4:7]
    
    context = {'key':'Home', 'service':service, 'home':home, 'latest_post':latest_post}
    return render(request, 'frontend/index.html', context)

def newsletter(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe = Newsletter.objects.create(email=email)
        subscribe.save()
        success = "Hello "+email+", your subscription has been confirmed. You've been added to our list and will hear from us soon."
        return HttpResponse(success)

def about(request):
    about       = About.objects.all()

    context = {'key':'About Us', 'about':about}
    return render(request, 'frontend/about.html', context)


def search(request):
    search = request.GET.get('search')
    if search:
        post = Post.objects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search) |
            Q(tags__name__icontains=search) |
            Q(author__username__icontains=search) |
            Q(date_created__icontains=search) 
        ).distinct()

        paginator = Paginator(post, 4)
        page = request.GET.get('page', 1)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        context = {'key':'Search Result', 'post':post, 'search':search}
        return render(request, 'blog/search.html', context)
    else:
        post = Post.objects.all()
        context = {'key':'Search Result'}
        return render(request, 'blog/search.html', context)


def tags(request, slug):
    tags    = get_object_or_404(Tags, slug=slug)
    post    = tags.tags.all()
    
    paginator = Paginator(post, 4)
    page = request.GET.get('page', 1)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {'key':'Post Tags', 'post':post}
    return render(request, 'blog/tags.html', context)

def category(request, slug):
    category    = get_object_or_404(Category, slug=slug)
    post        = category.category.all()

    paginator = Paginator(post, 4)
    page = request.GET.get('page', 1)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {'key':'Post Category', 'post':post}
    return render(request, 'blog/category.html', context)


def service(request):
    service = Service.objects.all()

    context = {'key':'Our Services', 'service':service}
    return render(request, 'frontend/service.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)

    context = {'key':'Service Detail', 'service':service}
    return render(request, 'frontend/service_detail.html', context)

def post(request):
    post = Post.objects.filter(status=1).order_by("-date_created")
  
    paginator   = Paginator(post, 4)
    page        = request.GET.get('page', 1)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {'key':'Post', 'post':post, 'page':page}
    return render(request, 'blog/post.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.view_count = post.view_count + 1
    post.last_view = datetime.now()
    post.save()

    category = Category.objects.get(id=post.category.id)
    related = category.category.all()

    if request.method == "POST":
        commentForm = CommentForm(request.POST or None)
        if commentForm.is_valid():
            body = commentForm.cleaned_data.get('body')
            commenter = request.user
            comment = Comment.objects.create(commenter=commenter, body=body, post=post)
            comment.save()
        return redirect('post_detail', slug=slug)

    replyForm = ReplyForm()
    commentForm = CommentForm()
    signinForm = SignInForm()
    signupForm = SignUpForm()

    context = {'key':'Post Detail', 'post':post, 'related':related, 'commentForm':commentForm, 'replyForm':replyForm, 'signinForm': signinForm, 'signupForm':signupForm}
    return render(request, 'blog/post_detail.html', context)


def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        replyForm = ReplyForm(request.POST or None)
        if replyForm.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            body = replyForm.cleaned_data.get('body')
            replier = request.user
            reply = Reply.objects.create(replier=replier, body=body, comment=comment)
            reply.save()
    return redirect('post_detail', slug=post.slug)


def likes_comment(request, id):
    user = request.user
    Like = False
    if request.method == "POST":
        commentlikes_id = request.POST['commentlikes_id']
        get_likes = get_object_or_404(Comment, id=commentlikes_id)

        if user in get_likes.comment_likes.all():
            get_likes.comment_likes.remove(user)
            Like = False
        else:
            get_likes.comment_likes.add(user)
            Like = True
        data = {
            'liked': Like,
            'likes_count': get_likes.comment_likes.all().count()
        }
        
        return JsonResponse(data, safe=False)
    return redirect(reverse('post_detail', args=[str(slug)]))


def dislikes_comment(request, id):
    user = request.user
    Dislike = False
    if request.method == "POST":
        commentdislike_id = request.POST['commentdislike_id']
        get_dislikes = get_object_or_404(Comment, id=commentdislike_id)

        if user in get_dislikes.comment_dislikes.all():
            get_dislikes.comment_dislikes.remove(user)
            Dislike = False
        else:
            get_dislikes.comment_dislikes.add(user)
            Dislike = True
        data = {
            'disliked':Dislike,
            'dislikes_Count': get_dislikes.comment_dislikes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('post_detail', args=[str(slug)]))


def likes_reply(request, id):
    user = request.user
    Like = False
    if request.method == "POST":
        replylikes_id = request.POST['replylikes_id']
        get_likes = get_object_or_404(Reply, id=replylikes_id)

        if user in get_likes.reply_likes.all():
            get_likes.reply_likes.remove(user)
            Like = False
        else:
            get_likes.reply_likes.add(user)
            Like = True
        data = {
            'replylikes': Like,
            'replylikes_count': get_likes.reply_likes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('post_detail', args=[str(slug)]))


def dislikes_reply(request, id):
    user = request.user
    Dislike = False
    if request.method == "POST":
        dislikesreply_id = request.POST['dislikesreply_id']
        get_dislikes = get_object_or_404(Reply, id=dislikesreply_id)

        if user in get_dislikes.reply_dislikes.all():
            get_dislikes.reply_dislikes.remove(user)
            Dislike = False
        else:
            get_dislikes.reply_dislikes.add(user)
            Dislike = True
        data = {
            'replydislikes': Dislike,
            'replydislikes_count': get_dislikes.reply_dislikes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('post_detail', args=[str(slug)]))


def team(request):
    team = Team.objects.all().order_by("team")

    paginator = Paginator(team, 10)
    page = request.GET.get('page')

    try:
        team = paginator.page(page)
    except PageNotAnInteger:
        team = paginator.page(1)
    except EmptyPage:
        team = paginator.page(paginator.num_pages)

    context = {'key':'Team', 'team':team}
    return render(request, 'frontend/team.html', context)

def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)

    context = {'key':'Team', 'team':team}
    return render(request, 'frontend/team_detail.html', context)

def career(request):
    career = Career.objects.all()

    paginator = Paginator(career, 10)
    page = request.GET.get('page', 1)

    try:
        career = paginator.page(page)
    except PageNotAnInteger:
        career = paginator.page(paginator.num_pages)

    context = {'key':'Career Opportunity', 'career':career}
    return render(request, 'frontend/career.html', context)

def career_detail(request, slug):
    career = get_object_or_404(Career, slug=slug)

    context = {'key':'Career Opportunity', 'career':career}
    return render(request, 'frontend/career_detail.html', context)

def faq(request):
    faq = Faq.objects.all()
    context = {'key':'Frequent Asked Questions', 'faq':faq}
    return render(request, 'frontend/faq.html', context)


def gallery(request):
    gallery = Gallery.objects.all().order_by("-title")
    context = {'key':'Photo Speaks', 'gallery':gallery}
    return render(request, 'frontend/gallery.html', context)


def contact(request):
    detail  = ContactDetail.objects.all()

    contactForm = ContactForm
    if request.method == "POST":
        form = contactForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["name"]
            messages.success(request, f"Dear { username }, We have received your message and would like to thank you for writing to us. We will reply by email as soon as possible.")
            form.save()

            name    = request.POST.get('name')
            email   = request.POST.get('email')
            subject = request.POST.get('subject')
            body    = request.POST.get('body')

            context = {
                "name": name,
                "email": email,
                "body": body,
            }

            template = get_template('frontend/contact.txt')
            content = template.render(context)

            email = EmailMessage(
                subject,
                content,
                "Sam Haruna Tech Team" + '',
                ['samharunaonline@gmail.com'],
                # ['samsonharuna@yahoo.com'],
                reply_to=[email],
                headers={'Message-ID': subject},
            )
            email.content_subtype = 'html'
            email.send()

    context = {'key':'Contact Page', 'contactForm':contactForm, 'detail':detail}
    return render(request, 'frontend/contact.html', context)


def blog_profile(request, username):
    profile = get_object_or_404(User, username=username)

    context = {'key':'Profile', 'profile':profile}
    return render(request, 'blog/blog_profile.html', context)


@login_required(login_url='loginapp')
def blog_viewprofile(request):    
    profile = get_object_or_404(User, id=request.user.id)
    post = Post.objects.filter(author=request.user)

    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    
    user = request.user.profile
    if request.method == "POST":
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Profile details were updated successfully')
            return redirect('blog_viewprofile')
        else:
            messages.info(request, 'Profile details were not updated successfully')
    else:
        profile_form = ProfileForm(instance=user)
    
    context = {'key':'Profile', 'profile':profile, 'post':post, 'profile_form':profile_form}
    return render(request, 'blog/blog_viewprofile.html', context)


@login_required(login_url='loginapp')
def blog_editname(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request, f'Account update for "{user}" was successful')
            return redirect('blog_editname')
        else:
            messages.info(request, 'Your account update was not successful')
    else:
        form = UserForm(instance=user)
    context = {'key':'Edit Name', 'form':form}
    return render(request, 'blog/blog_editname.html', context)


@login_required(login_url='loginapp')
def blog_changepassword(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password change was successful')
            return redirect('blog_changepassword')
        else:
            messages.info(request, 'Your password change was not successful')
    else:
        form = ChangePasswordForm(request.user)
    context = {'key':'Change Password', 'form':form}
    return render(request, 'blog/blog_changepassword.html', context)


@login_required(login_url='loginapp')
def blog_view(request):
    blog = Post.objects.filter(author=request.user)

    paginator = Paginator(blog, 12)
    page = request.GET.get('page')

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {'key':'Author Post', 'post':post}
    return render(request, 'blog/blog_view.html', context)


@login_required(login_url='loginapp')
def blog_form(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(request, 'Post was added successfully')
            return redirect('blog_view')
        else:
            messages.success(request, 'Post was not added successfully')
    else:
        form = PostForm()
    context = {'key':'Upload Post', 'form':form}
    return render(request, 'blog/blog_form.html', context)


@login_required(login_url='loginapp')
def blog_edit(request, slug):
    blog = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post was updated successfully')
            return redirect('blog_view')
        else:
            messages.success(request, 'Post was not updated successfully')
    else:
        form = PostForm(instance=blog)
    context = {'key':'Edit Post', 'form':form}
    return render(request, 'blog/blog_edit.html', context)


@login_required(login_url='loginapp')
def blog_delete(request, slug):
    blog = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        blog.delete()
        messages.success(request, 'Post was deleted Successfully')
        return redirect('blog_view')
    context = {'key':'Delete Post', 'item':blog}
    return render(request, 'blog/blog_delete.html', context)