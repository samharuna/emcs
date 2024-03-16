from django import forms
from account.models import User
from frontend.models import Tags, Category, About, News, Services, Blog, Testimonial, Contact, Details, Advert, Statement, Career, Header, Footer, Faq, Privacy, ServiceHeader, FAQHeader, TestimonialHeader, AboutHeader, ContactHeader, CareerHeader, Steps
from phonenumber_field.formfields import PhoneNumberField


class TagsForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label="Tag", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Post Tag Here ...', 'type':'text'}))
    
    class Meta:
        model = Tags
        fields = ['name',]
        error_class = 'error'
        
        
class CategoryForm(forms.ModelForm):
    tags            = forms.ModelChoiceField(queryset=Tags.objects.all(), label="Tag", empty_label="Select Post Tags Here", widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    name            = forms.CharField(max_length=100, label="Category", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Post Category Here ...', 'type':'text'}))
    
    class Meta:
        model = Category
        fields = ['tags', 'name']
        error_class = 'error'
        
        
class AboutForm(forms.ModelForm):
    description     = forms.CharField(max_length=200, label="About Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter About Description Here ...', 'type':'text'}))
    
    class Meta:
        model = About
        fields = ['image', 'description', 'body']
        error_class = 'error'
        
    
class ServicesForm(forms.ModelForm):
    category        = forms.ModelChoiceField(queryset=Category.objects.all(), label="Service Category", empty_label="Select Service Category Here", widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    description     = forms.CharField(max_length=255, label="Service Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Service Description Here ...', 'type':'text'}))
    
    class Meta:
        model = Services
        fields = ['image', 'category', 'description', 'body']
        error_class = 'error'
        
        
class BlogForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Blog Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Blog Title Here ...', 'type':'text'}))
    description     = forms.CharField(max_length=200, label="Blog Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Blog Description Here ...', 'type':'text'}))
    category        = forms.ModelChoiceField(queryset=Category.objects.all(), label="Blog Category", empty_label="Select Post Category Here", widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    
    class Meta:
        model = Blog
        fields = ['image', 'title', 'description', 'category', 'body']
        exclude = ['author',]
        error_class = 'error'
        
        
class StatusBlogForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Blog Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Blog Title Here ...', 'type':'text'}))
    description     = forms.CharField(max_length=200, label="Blog Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Blog Description Here ...', 'type':'text'}))
    author          = forms.ModelChoiceField(queryset=User.objects.all(), label="Blog Author", empty_label="Select Post Author Here", widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))
    category        = forms.ModelChoiceField(queryset=Category.objects.all(), label="Blog Category", empty_label="Select Post Category Here", widget=forms.Select(attrs={'class':'form-select', 'type':'select'}))

    class Meta:
        model = Blog
        fields = ['image', 'title', 'description', 'category', 'body', 'author', 'status']
        error_class = 'error'

        
class ContactForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name Here ...', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label="Email Address", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address Here ...', 'type':'email'}))
    subject         = forms.CharField(max_length=200, label="Subject", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Subject Here ...', 'type':'text'}))
    body            = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type The Message Here', 'rows':4, 'cols': 6, 'type':'textarea'}))
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'body']
        error_class = 'error'
        
                
class DetailsForm(forms.ModelForm):
    description     = forms.CharField(max_length=200, label="Contact Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Contact Detail Description Here ...', 'type':'text'}))
    address         = forms.CharField(max_length=255, label="Contact Office Address", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Main Office Address Here ...', 'type':'text'}))
    email           = forms.EmailField(max_length=100, label="Contact Email Address", widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Office Email Address Here ...', 'type':'email'}))
    branch          = forms.CharField(max_length=255, label="Contact Branch Address", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Branch Office Address Here ...', 'type':'text'}))
    phone           = PhoneNumberField(max_length=17, label="Contact Phone Number", region='NG', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number Here ...'}))
    mobile          = PhoneNumberField(max_length=17, label="Contact Mobile Number", region='NG', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Mobile Number Here ...'})) 
    starts          = forms.CharField(max_length=20, label="Resumption Time", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Resumption Time Here ...', 'type':'text'}))
    closes          = forms.CharField(max_length=20, label="Closing Time", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Closing Time Here ...', 'type':'text'}))
    direction       = forms.URLField(max_length=500, required=False, label='Contact Map Direction URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Map Direction URl Here ...', 'type':'url'}))
    facebook        = forms.URLField(max_length=500, required=False, label='Contact Facebook URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Facebook URL Here ...', 'type':'url'}))
    twitter         = forms.URLField(max_length=500, required=False, label='Contact Twitter URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Twitter URL Here ...', 'type':'url'}))
    instagram       = forms.URLField(max_length=500, required=False, label='Contact Instagram URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Instagram URL Here ...', 'type':'url'}))
    linkedin        = forms.URLField(max_length=500, required=False, label='Contact Linkedin URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Linkedin URL Here ...', 'type':'url'}))
    whatsapp        = forms.URLField(max_length=500, required=False, label='Contact WhatsApp URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter WhatsApp URL Here ...', 'type':'url'}))
    youtube         = forms.URLField(max_length=500, required=False, label='Contact Youtube URL', widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Youtube URL Here ...', 'type':'url'}))
    class Meta:
        model = Details
        fields = ['description', 'address', 'branch', 'starts', 'closes', 'phone', 'mobile', 'email', 'direction', 'facebook', 'twitter', 'instagram', 'linkedin', 'whatsapp', 'youtube']
        error_class = 'error'
        

class TestimonialForm(forms.ModelForm):
    name            = forms.CharField(max_length=100, label="Testifier Full Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Testifier Name Here ...', 'type':'text'}))
    occupation      = forms.CharField(max_length=200, label="Testifier Occupation", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Testifier Occupation Here ...', 'type':'text'}))
    
    class Meta:
        model = Testimonial
        fields = ['image', 'name', 'occupation', 'body']
        error_class = 'error'
    

class AdvertForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Advert Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Advert Title Here ...', 'type':'text'}))
    advert_url      = forms.URLField(max_length=500, label='Advert URL', required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter Advert URL Here ...', 'type':'url'}))
   
    class Meta:
        model = Advert
        fields = ['image', 'title', 'advert_url']
        error_class = 'error'
        
class StatementForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Statement Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Statement Title Here ...', 'type':'text'}))
    
    class Meta:
        model = Statement
        fields = ['title', 'body']
        error_class = 'error'
        
        
class CareerForm(forms.ModelForm):
    position        = forms.CharField(max_length=100, label="Vacant Position", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Position Title Here ...', 'type':'text'}))
    description     = forms.CharField(max_length=200, label="Vacant Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Position Description Here ...', 'type':'text'}))
    
    class Meta:
        model = Career
        fields = ['image', 'position', 'description', 'body']
        error_class = 'error'


class NewsForm(forms.ModelForm):
    title           = forms.CharField(max_length=255, label="News Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter News Title Here ...', 'type':'text'}))
    
    class Meta:
        model = News
        fields = ['title',] 
        error_class = 'error'
        
        
class HeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = Header
        fields = ['image', 'title']
        error_class = 'error'
        
        
class FooterForm(forms.ModelForm):
    title           = forms.CharField(max_length=100, label="Footer Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Footer Title Here ...', 'type':'text'}))
   
    class Meta:
        model = Footer
        fields = ['image', 'title']
        error_class = 'error'
        
        
class FaqForm(forms.ModelForm):
    title               = forms.CharField(max_length=140, label='FAQ Title:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter FAQ Title', 'type':'text'}))
    
    class Meta:
        model = Faq
        fields = ['title', 'body']
        error_class = 'error'
        
        
class PrivacyForm(forms.ModelForm):
    title               = forms.CharField(max_length=110, label='Privacy Title:', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Privacy Title', 'type':'text'}))
    
    class Meta:
        model = Privacy
        fields = ['title', 'body']
        error_class = 'error'
        

class ServiceHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="Service Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
   
    class Meta:
        model = ServiceHeader
        fields = ['title',] 
        error_class = 'error'
        

class FAQHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="FAQ Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = FAQHeader
        fields = ['title',] 
        error_class = 'error'
        
        
class TestimonialHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="Testimonial Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = TestimonialHeader
        fields = ['title',] 
        error_class = 'error'
        

class AboutHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="About Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = AboutHeader
        fields = ['title',] 
        error_class = 'error'
        

class ContactHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="Contact Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = ContactHeader
        fields = ['title',] 
        error_class = 'error'
        

class CareerHeaderForm(forms.ModelForm):
    title           = forms.CharField(max_length=200, label="Career Header Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Header Title Here ...', 'type':'text'}))
    
    class Meta:
        model = CareerHeader
        fields = ['title',] 
        error_class = 'error'
        

class StepsForm(forms.ModelForm):
    serial_number   = forms.CharField(max_length=10, label="Loan Step Serial Number", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Step Serial Number Here ...', 'type':'number'}))
    title           = forms.CharField(max_length=200, label="Loan Step Title", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Step Title Here ...', 'type':'text'}))
    description     = forms.CharField(max_length=200, label="Loan Step Description", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Loan Step Description Here ...', 'type':'text'}))

    class Meta:
        model = Steps
        fields = ['serial_number', 'title', 'description'] 
        error_class = 'error'