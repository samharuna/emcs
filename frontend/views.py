from django.shortcuts import render, redirect, get_object_or_404
from maintenance_mode.decorators import force_maintenance_mode_off, force_maintenance_mode_on
from frontend.models import Tags, Category, About, News, Services, Blog, Privacy, Testimonial, Contact, Details, Advert, Statement, Career, Header, Footer, Faq
from frontend.forms import ContactForm
from django.db.models import Q
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string, get_template

# Create your views here.
def home(request):
    home = Services.objects.all()
    context = {'key':'Home', 'home':home}
    return render(request, 'frontend/home/index.html', context)

def about(request):
    about = About.objects.all()
    statement = Statement.objects.all()
    context = {'key':'About', 'about':about, 'statement':statement}
    return render(request, 'frontend/about/about.html', context)

def about_detail(request, slug):
    about = get_object_or_404(About, slug=slug)
    context = {'key':'About Detail', 'about':about}
    return render(request, 'frontend/about/about_detail.html', context)

def service(request):
    service = Services.objects.all()
    context = {'key':'Service', 'service':service}
    return render(request, 'frontend/services/service.html', context)

def service_detail(request, slug):
    services = get_object_or_404(Services, slug=slug)

    context = {'key':'Service Detail', 'services':services}
    return render(request, 'frontend/services/service_detail.html', context)

def tags(request, slug):
    tags    = get_object_or_404(Tags, slug=slug)
    post    = tags.tags.all()

    context = {'key':'Post Tags', 'post':post}
    return render(request, 'blog/tags.html', context)

def category(request, slug):
    category    = get_object_or_404(Category, slug=slug)
    post        = category.category.all()

    context = {'key':'Post Category', 'post':post}
    return render(request, 'blog/category.html', context)

def career(request):
    career = Career.objects.all()
    
    context = {'key':'Career Opportunity', 'career':career}
    return render(request, 'frontend/career/career.html', context)

def career_detail(request, slug):
    career = get_object_or_404(Career, slug=slug)
   
    context = {'key':'Career Opportunity', 'career':career}
    return render(request, 'frontend/career/career_detail.html', context)

def faq(request):
    faq = Faq.objects.all()
    context = {'key':'FAQ', 'faq':faq}
    return render(request, 'frontend/faq/faq.html', context)

def privacy(request):
    privacy = Privacy.objects.all()
    context = {'key':'Privacy', 'privacy':privacy}
    return render(request, 'frontend/privacy/privacy.html', context)

def contact(request):
    contactForm = ContactForm
    if request.method == "POST":
        form = contactForm(data=request.POST or None)
        if form.is_valid():
            
            username = form.cleaned_data["name"]
            messages.success(request, f"Dear { username }, we have received your message and would like to thank you for writing to us. We will reply by email as soon as possible.")
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

            template = get_template('frontend/contact/contact.txt')
            content = template.render(context)

            email = EmailMessage(
                subject,
                content,
                "EMCS Support Team" + '',
                ['emcsonline247@gmail.com'],
                reply_to=[email],
                headers={'Message-ID': subject},
            )
            email.content_subtype = 'html'
            email.send()
        
        else:
            form.errors
            messages.warning(request, 'Your message to Empower Multipurpose Cooperative Society was not sent, please rectify the errors')

    context = {'key':'Contact Us', 'contactForm':contactForm}
    return render(request, 'frontend/contact/contact.html', context)


# Start of Error 404
def handle_404_error(request, exception):
    context = {'title': 'Error 404'}
    return render(request, 'errors/error_404.html', context)
# End of Error 404


# Start of Error 505
def handle_500_error(request):
    context = {'title': 'Error 500'}
    return render(request, 'errors/error_500.html', context)
# End of Error 404








