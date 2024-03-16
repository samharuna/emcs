from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django_pandas.io import read_frame
from newsletter.models import Subscriber, SendMessage, Mails
from newsletter.forms import SubscriberForm, SendMessageForm, MailsForm
from backend.decorators import allowed_users
from account.models import User

# Create your views here.
def newsletter(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe = Subscriber.objects.create(email=email)
        subscribe.save()
        success = "Your subscription has been confirmed. You've been added to our list and will hear from us soon."
        return HttpResponse(success)
    
@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def send_message(request):
    emails      = Subscriber.objects.all()
    df          = read_frame(emails, fieldnames=['email'])
    mail_list   = df['email'].values.tolist()
    if request.method == "POST":
        form = SendMessageForm(request.POST or None)
        if form.is_valid():
            form.save()
            
            subject = request.POST['subject']
            body    = request.POST['body']
            send_mail(
                subject,
                body,
                "",
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Message to the subscriber lists was sent successfully')
            return redirect('view-message')
        else:
            form.errors
            messages.warning(request, 'Message to the subscriber lists was not sent')
    else:
        form = SendMessageForm()
    context = {'title':'Send Message', 'form':form,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/message/send_message.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_message(request):
    sendMessage = SendMessage.objects.all()
    context = {'title':'View Message', 'sendMessage':sendMessage,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/message/view_message.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_message(request, slug):
    emails      = Subscriber.objects.all()
    df          = read_frame(emails, fieldnames=['email'])
    mail_list   = df['email'].values.tolist()
    sendMessage = get_object_or_404(SendMessage, slug=slug)
    if request.method == "POST":
        form = SendMessageForm(request.POST, instance=sendMessage)
        if form.is_valid():
            form.save()
            subject = request.POST['subject']
            body    = request.POST['body']
            send_mail(
                subject,
                body,
                "",
                mail_list,
                fail_silently=False,
            )
            messages.success(request, 'Message to the subscriber lists was updated successfully')
            return redirect('view-message')
        else:
            form.errors
            messages.warning(request, 'Message to the subscriber lists was not updated')
    else:
        form = SendMessageForm(instance=sendMessage)
    context = {'title':'Edit Message', 'form':form, 'sendMessage':sendMessage,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/message/edit_message.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_message(request, slug):
    sendMessage = get_object_or_404(SendMessage, slug=slug)
    if request.method == "POST":
        sendMessage.delete()
        messages.success(request, 'Message to the subscriber lists was deleted successfully')
        return redirect('view-message')
    context = {'title':'Delete Message', 'sendMessage':sendMessage,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/message/delete_message.html', context)



@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def view_subscriber(request):
    subscriber = Subscriber.objects.all()
    context = {'title':'View Subscribers', 'subscriber':subscriber,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/subscribers/view_subscriber.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def edit_subscriber(request, slug):
    subscriber = get_object_or_404(Subscriber, slug=slug)
    if request.method == "POST":
        form = SubscriberForm(request.POST or None, instance=subscriber)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscriber Email Address was updated successfully')
            return redirect('view-subscriber')
        else:
            form.errors
            messages.warning(request, 'Subscriber Email Address was not updated')
    else:
        form = SubscriberForm(instance=subscriber)
    context = {'title':'Edit Subscriber', 'subscriber':subscriber, 'form':form}
    return render(request, 'newsletter/subscribers/edit_subscriber.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff"])
def delete_subscriber(request, slug):
    subscriber = get_object_or_404(Subscriber, slug=slug)
    if request.method == "POST":
        subscriber.delete()
        messages.success(request, 'Subscriber Email Address was deleted successfully')
        return redirect('view-subscriber')
    context = {'title':'Delete Subscriber', 'subscriber':subscriber,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/subscribers/delete_subscriber.html', context)



@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def send_mails(request, slug):
    recipient = get_object_or_404(User, slug=slug)
    sender = request.user
    
    if request.method == "POST":
        form = MailsForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.recipient = recipient
            instance.sender = sender
            instance.save()
            messages.success(request, 'Your message was sent successfully')
            return redirect('profile', recipient.slug)
        else:
            form.errors
            messages.warning(request, 'Your Message sent was not successful')
    else:
        form = MailsForm()
        
    context = {'title':'Compose Mail', 'form':form, 'recipient':recipient,
                'mails':request.user.recipient.all(), 'sender':sender,
                'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/mails/mail_compose.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def view_mails(request):
    user = request.user
    mails = user.recipient.all()
    mails_count = mails.filter(is_read=False).count()

    context = {'title':'View Mails', 'mails':mails, 'mails_count':mails_count}
    return render(request, 'newsletter/mails/mailbox.html', context)

@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def detail_mails(request, slug):
    mail = get_object_or_404(Mails, slug=slug)
    
    if mail.is_read == False:
        mail.is_read = True
        mail.save()
    
    context = {'title':'Mail Detail', 'mail':mail,
               'mails':request.user.recipient.all(), 
               'mails_count':request.user.recipient.all().filter(is_read=False).count()}
    return render(request, 'newsletter/mails/mail_view.html', context)


@login_required(login_url='sign-in')
@allowed_users(allowed_roles=["admin", "staff", "customer"])
def delete_mails(request, slug):
    mails = get_object_or_404(Mails, slug=slug)
    mails.delete()
    messages.success(request, 'Your Message was deleted successfully')
    return redirect('view-mails')





